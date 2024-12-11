// threadpool.c
#include <Python.h>
#include "threadpool.h"
#include <stdlib.h>
#include <string.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
// a single unit of work, contains all information a thread would need
// like which func to use, what's the arg, buffer to store information, index
// for location information (important)


pthread_mutex_t log_lock = PTHREAD_MUTEX_INITIALIZER;

int dval = 1;
// thread-safe logging that flushes stdout after printing
void log_message(const char *format, ...) {
    if (dval == 0) {
        va_list args;
        va_start(args, format);
        pthread_mutex_lock(&log_lock);
        vprintf(format, args);
        fflush(stdout);
        pthread_mutex_unlock(&log_lock);
        va_end(args);
    }
}


ThreadPool* thread_pool_init(int thread_count, size_t initial_elements) {
    // printf("initialized a thread pool\n");
    
    ThreadPool *pool;
    int i;

    
    if (thread_count <= 0 || initial_elements == 0) {
        fprintf(stderr, "Invalid thread count or initial elements.\n");
        return NULL;
    }

   
    if ((pool = (ThreadPool *)malloc(sizeof(ThreadPool))) == NULL) {
        goto err;
    }

   
    pool->thread_count = 0;
    pool->started = 0;
    pool->stop = 0;
    pool->head = pool->tail = NULL;
    pool->completed_tasks = 0;
    pool->total_elements = initial_elements;

    if ((pool->threads = (pthread_t *)malloc(sizeof(pthread_t) * thread_count)) == NULL) {
        goto err;
    }

    if ((pool->results = (char **)calloc(initial_elements, sizeof(char *))) == NULL) {
        goto err;
    }

    if ((pool->result_sizes = (size_t *)calloc(initial_elements, sizeof(size_t))) == NULL) {
        goto err;
    }

    if ((pool->task_statuses = (int *)calloc(initial_elements, sizeof(int))) == NULL) {
        goto err;
    }

    if (pthread_mutex_init(&(pool->lock), NULL) != 0) {
        goto err;
    }

    if (pthread_cond_init(&(pool->notify), NULL) != 0) {
        pthread_mutex_destroy(&(pool->lock));
        goto err;
    }

    if (pthread_cond_init(&(pool->completed), NULL) != 0) {
        pthread_mutex_destroy(&(pool->lock));
        pthread_cond_destroy(&(pool->notify));
        goto err;
    }

    // Start worker threads
    for (i = 0; i < thread_count; i++) {
        if (pthread_create(&(pool->threads[i]), NULL, thread_do_work, (void*)pool) != 0) {
            thread_pool_destroy(pool);
            return NULL;
        }
        pool->thread_count++;
        pool->started++;
    }
    // printf("spawned %zu == %zu threads\n", pool->thread_count, pool->started);

    return pool;

err:
    if (pool) {
        pthread_mutex_destroy(&(pool->lock));
        pthread_cond_destroy(&(pool->notify));
        pthread_cond_destroy(&(pool->completed));
        free(pool->threads);
        free(pool->results);
        free(pool->result_sizes);
        free(pool);
    }
    return NULL;
}


int thread_pool_add_pickle_task(ThreadPool *pool, task_func function, void *object, size_t index) {
    
    Task *task;

    if (pool == NULL || function == NULL || index >= pool->total_elements) {
        return -1;
    }

    if ((task = (Task *)malloc(sizeof(Task))) == NULL) {
        return -1;
    }
    
    task->function = function;
    task->arg = object;
    task->index = index;
    task->output = NULL;
    task->output_size = 0;
    task->next = NULL;

    pthread_mutex_lock(&(pool->lock));

    if (pool->stop) {
        pthread_mutex_unlock(&(pool->lock));
        free(task);
        return -1;
    }

       
    if (pool->tail == NULL) {
        pool->head = pool->tail = task;
        // printf("successfully did  pool->head = pool->tail = task;\n");
    } else {
        pool->tail->next = task;
        pool->tail = task;
        // printf("successfullymoved head to the next pointer\n");
    }

    // signal to thread to let it know that a new task is available

    pthread_cond_signal(&(pool->notify));
    // printf("signal check\n");
    pthread_mutex_unlock(&(pool->lock));
    // printf("unlocked mutex\n");
    // printf("added a pickling task to our taskqueue\n");
    return 0;
}

int thread_pool_destroy(ThreadPool *pool) {
    size_t i;
    Task *task;

    if (pool == NULL) {
        return -1;
    }

    pthread_mutex_lock(&(pool->lock));
    pool->stop = 1;
    pthread_cond_broadcast(&(pool->notify));
    pthread_mutex_unlock(&(pool->lock));

    for (i = 0; i < pool->thread_count; i++) {
        pthread_join(pool->threads[i], NULL);
    }

    // Free remaining tasks
    while (pool->head != NULL) {
        task = pool->head;
        pool->head = task->next;
        free(task);
    }

    pthread_mutex_destroy(&(pool->lock));
    pthread_cond_destroy(&(pool->notify));
    pthread_cond_destroy(&(pool->completed));

    free(pool->threads);
    for (i = 0; i < pool->total_elements; i++) {
        free(pool->results[i]);
    }
    free(pool->results);
    free(pool->result_sizes);
    free(pool->task_statuses);
    free(pool);

    return 0;
}


void *thread_do_work(void *pool) {
    ThreadPool *thread_pool = (ThreadPool *)pool;
    Task *task;

    while (1) {
        pthread_mutex_lock(&(thread_pool->lock));

        while ((thread_pool->head == NULL) && (!thread_pool->stop)) {
            pthread_cond_wait(&(thread_pool->notify), &(thread_pool->lock));
        }

        if (thread_pool->stop && thread_pool->head == NULL) {
            pthread_mutex_unlock(&(thread_pool->lock));
            break;
        }

        task = thread_pool->head;
        if (task != NULL) {
            thread_pool->head = task->next;
            if (thread_pool->head == NULL) {
                thread_pool->tail = NULL;
            }
        }

        pthread_mutex_unlock(&(thread_pool->lock));

        if (task != NULL) {
        
            // PyGILState_STATE gstate = PyGILState_Ensure();

            log_message("Thread %lu: Starting task at index %zu\n", pthread_self(), task->index);
            int result = (*(task->function))(task->arg, &task->output, &task->output_size);
            log_message("Thread %lu: Finished task at index %zu with result %d\n", pthread_self(), task->index, result);
           

            // update the thread pool state
            pthread_mutex_lock(&(thread_pool->lock));
            if (result == 0) {
                thread_pool->results[task->index] = task->output;
                thread_pool->result_sizes[task->index] = task->output_size;
                thread_pool->task_statuses[task->index] = 0; // Success
            } else {
                thread_pool->task_statuses[task->index] = -1; // Failure
            }
            thread_pool->completed_tasks++;
            if (thread_pool->completed_tasks == thread_pool->total_elements) {
                pthread_cond_signal(&(thread_pool->completed));
            }
            pthread_mutex_unlock(&(thread_pool->lock));

            free(task);
        }
    }

    pthread_mutex_lock(&(thread_pool->lock));
    thread_pool->started--;
    pthread_mutex_unlock(&(thread_pool->lock));

    pthread_exit(NULL);
    return NULL;
}



char *thread_pool_get_serialized_result(ThreadPool *pool, size_t *total_size) {
    char *final_result = NULL;
    *total_size = 0;


    for (size_t i = 0; i < pool->total_elements; i++) {
        *total_size += pool->result_sizes[i];
    }

    final_result = (char *)malloc(*total_size);
    if (final_result == NULL) {
        return NULL;
    }

    char *current_pos = final_result;
    for (size_t i = 0; i < pool->total_elements; i++) {
        if (pool->results[i] != NULL) {
            memcpy(current_pos, pool->results[i], pool->result_sizes[i]);
            current_pos += pool->result_sizes[i];
        } else {
            
            fprintf(stderr, "Warning: Result for task %zu is NULL.\n", i);
        }
    }

    return final_result;
}


// block calling thread until we're done with all the tasks in the queue
int thread_pool_wait_completion(ThreadPool *pool) {
    pthread_mutex_lock(&(pool->lock));
    while (pool->completed_tasks < pool->total_elements) {
        pthread_cond_wait(&(pool->completed), &(pool->lock));
    }
    pthread_mutex_unlock(&(pool->lock));
    return 0;
}

 int thread_pool_get_task_status(ThreadPool *pool, size_t index) {
    if (index >= pool->total_elements) {
        return -1; // Invalid index
    }
    return pool->task_statuses[index];
}

char* thread_pool_get_individual_result(ThreadPool *pool, size_t index) {
    if (pool == NULL || index >= pool->total_elements) {
        return NULL;
    }

    pthread_mutex_lock(&(pool->lock));
    char *result = NULL;
    if (pool->results != NULL && pool->results[index] != NULL) {
        size_t size = pool->result_sizes[index];
        result = malloc(size);
        if (result != NULL) {
            memcpy(result, pool->results[index], size);
        } else {
            // Handle memory allocation failure
            fprintf(stderr, "Memory allocation failed in thread_pool_get_individual_result for index %zu.\n", index);
        }
    }
    pthread_mutex_unlock(&(pool->lock));

    return result;
}


size_t thread_pool_get_result_size(ThreadPool *pool, size_t index) {
    if (pool == NULL || index >= pool->total_elements) {
        return 0;
    }

    pthread_mutex_lock(&(pool->lock));
    size_t size = 0;
    if (pool->result_sizes != NULL) {
        size = pool->result_sizes[index];
    }
    pthread_mutex_unlock(&(pool->lock));

    return size;
}