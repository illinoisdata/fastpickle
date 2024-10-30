// threadpool.h

#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct ThreadPool ThreadPool;

// taskfunction: input object to process, pointer to a char* where serialized output is stored
//  size of serialized data
typedef int (*task_func)(void *object, char **output, size_t *output_size);
static void* thread_do_work(void* pool);
ThreadPool* thread_pool_init(int thread_count, size_t initial_elements);
int thread_pool_add_pickle_task(ThreadPool *pool, task_func function, void *object, size_t index);
int thread_pool_destroy(ThreadPool *pool);
char *thread_pool_get_serialized_result(ThreadPool *pool, size_t *total_size);
int thread_pool_wait_completion(ThreadPool *pool);

char* thread_pool_get_individual_result(ThreadPool *pool, size_t index);
size_t thread_pool_get_result_size(ThreadPool *pool, size_t index);

#ifdef __cplusplus
}
#endif

#endif // THREADPOOL_H
