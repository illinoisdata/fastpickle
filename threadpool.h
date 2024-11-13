#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <Python.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

//  structs used for the memoization table
typedef struct {
    PyObject *me_key;
    Py_ssize_t me_value;
} PyMemoEntry;

typedef struct {
    size_t mt_mask;
    size_t mt_used;
    size_t mt_allocated;
    PyMemoEntry *mt_table; 
    pthread_mutex_t mt_lock;  // Threads will hold onto this lock 
} PyMemoTable;

typedef int (*task_func)(void *object, char **output, size_t *output_size);

typedef struct Task {
    task_func function;  // Function pointer for our task (void *)
    void *arg;           // Argument for task function
    struct Task *next;   // Next task in queue
    size_t index;        // Index of our task, needed for result placement
    char *output;        // Output buffer for our task
    size_t output_size;  // Size of this data
} Task;

typedef struct ThreadPool {
    pthread_t *threads;             // Array of thread IDs
    size_t thread_count;               // Number of threads in the pool
    Task *head;                     // Head of the task queue
    Task *tail;                     // Tail of the task queue
    pthread_mutex_t lock;           // Mutex for task queue access
    pthread_cond_t notify;          // Condition variable for new tasks
    pthread_cond_t completed;       // Condition variable for task completion
    int stop;                       // Flag to indicate pool shutdown
    int started;                    // Number of active threads
    char **results;                 // Serialized results for each task
    size_t *result_sizes;           // Sizes of serialized results
    size_t total_elements;          // Total number of tasks
    size_t completed_tasks;         // Number of completed tasks
    int *task_statuses;             // Status of each task
    PyMemoTable *memo_table;        // Shared memoization table
} ThreadPool;


void* thread_do_work(void* pool);
ThreadPool* thread_pool_init(int thread_count, size_t initial_elements, PyMemoTable *memo_table);
int thread_pool_add_pickle_task(ThreadPool *pool, task_func function, void *object, size_t index);
int thread_pool_destroy(ThreadPool *pool);
char *thread_pool_get_serialized_result(ThreadPool *pool, size_t *total_size);
int thread_pool_wait_completion(ThreadPool *pool);
char* thread_pool_get_individual_result(ThreadPool *pool, size_t index);
size_t thread_pool_get_result_size(ThreadPool *pool, size_t index);
int thread_pool_get_task_status(ThreadPool *pool, size_t index);

#ifdef __cplusplus
}
#endif

#endif // THREADPOOL_H
