// gcc -o test_pickle testpickle.c threadpool.c -pthread

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "threadpool.h"

#define MEMO_TABLE_SIZE 1024

typedef struct Node {
    int value;
    struct Node *next;
} Node;
// similar to PyMemoTable
typedef struct MemoEntry {
    const void *ptr;
    char *serialized;
    struct MemoEntry *next;
} MemoEntry;

MemoEntry *memo_table[MEMO_TABLE_SIZE] = {0};
pthread_mutex_t memo_mutex = PTHREAD_MUTEX_INITIALIZER;

// Hash function for pointers
unsigned int ptr_hash(const void *ptr) {
    return ((unsigned long)ptr) % MEMO_TABLE_SIZE;
}

char *memo_get(const void *ptr) {
    unsigned int hash = ptr_hash(ptr);
    MemoEntry *entry = memo_table[hash];
    while (entry != NULL) {
        if (entry->ptr == ptr) {
            return entry->serialized;
        }
        entry = entry->next;
    }
    return NULL;
}

int memo_set(const void *ptr, char *serialized) {
    unsigned int hash = ptr_hash(ptr);
    MemoEntry *new_entry = (MemoEntry *)malloc(sizeof(MemoEntry));
    if (new_entry == NULL) {
        return -1;
    }
    new_entry->ptr = ptr;
    new_entry->serialized = serialized;
    new_entry->next = memo_table[hash];
    memo_table[hash] = new_entry;
    return 0;
}

int serialize_node(void *object, char **output, size_t *output_size) {
    Node *node = (Node *)object;
    char *serialized = NULL;

    pthread_mutex_lock(&memo_mutex);
    char *existing_serialization = memo_get(node);
    pthread_mutex_unlock(&memo_mutex);

    if (existing_serialization != NULL) {
        // Node has already been serialized, return a reference
        char next_ref[32];
        if (node->next == NULL) {
            snprintf(next_ref, sizeof(next_ref), "NULL");
        } else {
            snprintf(next_ref, sizeof(next_ref), "Ref(%p)", (void *)node->next);
        }

        if (asprintf(&serialized, "REFERENCE Node(value=%d, next=%s)", node->value, next_ref) == -1) {
            return -1;
        }
    } else {
        // Serialize the 'next' pointer as a reference
        char next_ref[32];
        if (node->next == NULL) {
            snprintf(next_ref, sizeof(next_ref), "NULL");
        } else {
            snprintf(next_ref, sizeof(next_ref), "Ref(%p)", (void *)node->next);
        }

        // Serialize this node
        if (asprintf(&serialized, "Node(value=%d, next=%s)", node->value, next_ref) == -1) {
            return -1;
        }

        // Add this node to the memoization table
        pthread_mutex_lock(&memo_mutex);
        if (memo_set(node, serialized) != 0) {
            pthread_mutex_unlock(&memo_mutex);
            free(serialized);
            return -1;
        }
        pthread_mutex_unlock(&memo_mutex);
    }

    // Set the output
    *output = serialized;
    *output_size = strlen(serialized);

    return 0;
}

int main() {
    // Create Nodes a, b, c
    Node *a = (Node *)malloc(sizeof(Node));
    Node *b = (Node *)malloc(sizeof(Node));
    Node *c = (Node *)malloc(sizeof(Node));

    if (a == NULL || b == NULL || c == NULL) {
        fprintf(stderr, "err.\n");
        return -1;
    }

    a->value = 1;
    b->value = 2;
    c->value = 3;

    a->next = a;
    b->next = c;
    c->next = a;

    Node *shared = a;

    //  [a, b, c, shared]
    Node *node_list[4] = {a,a,a,a};

    int thread_count = 3;
    size_t total_elements = 4;

    ThreadPool *pool = thread_pool_init(thread_count, total_elements);
    if (pool == NULL) {
        fprintf(stderr, "Error initializing thread pool\n");
        free(a);
        free(b);
        free(c);
        return -1;
    }

    for (size_t i = 0; i < total_elements; i++) {
        int rc = thread_pool_add_pickle_task(pool, serialize_node, node_list[i], i);
        if (rc != 0) {
            fprintf(stderr, "Error\n");
            thread_pool_destroy(pool);
            
            free(a);
            free(b);
            free(c);
            return -1;
        }
    }

    thread_pool_wait_completion(pool);

    printf("Serialized Result:\n");
    for (size_t i = 0; i < total_elements; i++) {
        char *serialized = thread_pool_get_individual_result(pool, i);
        if (serialized != NULL) {
            printf("Element %zu: %s\n", i, serialized);
            free(serialized); // Free the duplicated string
        } else {
            printf("Element %zu: <NULL>\n", i);
        }
    }

    // Alternatively, you can get the concatenated serialized result
    /*
    size_t total_size = 0;
    char *serialized_result = thread_pool_get_serialized_result(pool, &total_size);

    if (serialized_result == NULL) {
        fprintf(stderr, "Error getting serialized result\n");
        thread_pool_destroy(pool);
        // Free allocated nodes before exiting
        free(a);
        free(b);
        free(c);
        return -1;
    }

    printf("Serialized Result (Concatenated):\n%s\n", serialized_result);
    free(serialized_result);
    */

    // Clean up
    thread_pool_destroy(pool);

    // Free the Nodes
    free(a);
    free(b);
    free(c);

    // Clean up the memoization table
    for (int i = 0; i < MEMO_TABLE_SIZE; i++) {
        MemoEntry *entry = memo_table[i];
        while (entry != NULL) {
            MemoEntry *tmp = entry;
            entry = entry->next;
            // free(tmp->serialized);
            free(tmp);
        }
        memo_table[i] = NULL;
    }

    pthread_mutex_destroy(&memo_mutex);

    return 0;
}
