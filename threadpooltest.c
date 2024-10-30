#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "threadpool.h"

typedef struct {
    int value;
} Object;

typedef struct {
    pthread_mutex_t lock;
    size_t memo_id_counter;
    size_t capacity;
    Object **objects;
    size_t *memo_ids;
} MemoTable;

MemoTable memo_table;

void init_memo_table(size_t capacity) {
    pthread_mutex_init(&memo_table.lock, NULL);
    memo_table.memo_id_counter = 0;
    memo_table.capacity = capacity;
    memo_table.objects = (Object **)calloc(capacity, sizeof(Object *));
    memo_table.memo_ids = (size_t *)calloc(capacity, sizeof(size_t));
}

void destroy_memo_table() {
    pthread_mutex_destroy(&memo_table.lock);
    free(memo_table.objects);
    free(memo_table.memo_ids);
}


int get_or_assign_memo_id(Object *obj, size_t *memo_id) {
    pthread_mutex_lock(&memo_table.lock);
   
    for (size_t i = 0; i < memo_table.memo_id_counter; i++) {
        if (memo_table.objects[i] == obj) {
            *memo_id = memo_table.memo_ids[i];
            pthread_mutex_unlock(&memo_table.lock);
            return 1; 
        }
    }
    
    if (memo_table.memo_id_counter >= memo_table.capacity) {
      
        memo_table.capacity *= 2;
        memo_table.objects = (Object **)realloc(memo_table.objects, memo_table.capacity * sizeof(Object *));
        memo_table.memo_ids = (size_t *)realloc(memo_table.memo_ids, memo_table.capacity * sizeof(size_t));
    }
    memo_table.objects[memo_table.memo_id_counter] = obj;
    *memo_id = memo_table.memo_id_counter;
    memo_table.memo_ids[memo_table.memo_id_counter] = *memo_id;
    memo_table.memo_id_counter++;
    pthread_mutex_unlock(&memo_table.lock);
    return 0; 
}


int serialize_object(void *arg, char **output, size_t *output_size) {
    Object *obj = (Object *)arg;
    size_t memo_id;
    int is_memoized = get_or_assign_memo_id(obj, &memo_id);

    if (is_memoized) {
    
        const char *format = "GET %zu\n";
        *output_size = snprintf(NULL, 0, format, memo_id);
        *output = (char *)malloc(*output_size + 1);
        if (*output == NULL) {
            return -1;
        }
        snprintf(*output, *output_size + 1, format, memo_id);
    } else {
        
        const char *format = "PUT %zu OBJ %d\n";
        *output_size = snprintf(NULL, 0, format, memo_id, obj->value);
        *output = (char *)malloc(*output_size + 1);
        if (*output == NULL) {
            return -1;
        }
        snprintf(*output, *output_size + 1, format, memo_id, obj->value);
    }
    return 0;
}

int main() {
    
    init_memo_table(10);

    
    Object *a = (Object *)malloc(sizeof(Object));
    a->value = 1;
    Object *b = (Object *)malloc(sizeof(Object));
    b->value = 2;
    Object *c = a; 
    Object *d = b; 
    Object *e = a;
    Object *f = e;


    
    Object *object_list[12] = {c,d,f,e,b,a,a,a,a,a,a,a};
    size_t list_size = 12;

    
    int thread_count = 5;
    ThreadPool *pool = thread_pool_init(thread_count, list_size);
    if (pool == NULL) {
        fprintf(stderr, "Failed to initialize thread pool.\n");
        return -1;
    }

    
    for (size_t i = 0; i < list_size; i++) {
        if (thread_pool_add_pickle_task(pool, serialize_object, (void *)object_list[i], i) != 0) {
            fprintf(stderr, "Failed to add task to thread pool.\n");
            return -1;
        }
    }

    
    thread_pool_wait_completion(pool);

    
    size_t total_size;
    char *serialized_data = thread_pool_get_serialized_result(pool, &total_size);
    if (serialized_data == NULL) {
        fprintf(stderr, "Failed to get serialized result.\n");
        return -1;
    }

    printf("Serialized Data:\n%s", serialized_data);

    free(serialized_data);
    thread_pool_destroy(pool);
    destroy_memo_table();
    free(a);
    free(b);

    return 0;
}

