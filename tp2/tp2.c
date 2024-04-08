#include "tp2.h"
#include <stdlib.h>
#include <stdbool.h>

struct node;
typedef struct node node_t;

struct node {
    void* value;
    node_t* next;
    node_t* prev;
};

struct list {
    node_t* head;
    node_t* tail;
    size_t size;
};

struct list_iter {
    list_t* list;
    node_t* curr;
};

list_t *list_new(){
    list_t* list = malloc(sizeof(list_t));
    if (list == NULL) return NULL;
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
    return list;
}

size_t list_length(const list_t *list){
    if (list == NULL) return 0;
    return list->size;
}

bool list_is_empty(const list_t *list){
    if (list == NULL) return NULL;
    return list->size == 0;
}

bool list_insert_head(list_t *list, void *value){
    if (list == NULL) return false;
    
    node_t* node = malloc(sizeof(node_t));
    if (node == NULL) return false;

    node->prev = NULL;
    node->next = list->head;
    node->value = value;

    if (list->head != NULL) list->head->prev = node;
    if (list->tail == NULL) list->tail = node;
    list->head = node;
    list->size++;

    return true;
}

bool list_insert_tail(list_t *list, void *value){
    if (list == NULL) return false;

    node_t* node = malloc(sizeof(node_t));
    if (node == NULL) return false;
    node->value = value;
    node->next = NULL;
    node->prev = list->tail;

    if (list->tail != NULL) list->tail->next = node;
    if (list->head == NULL) list->head = node;
    list->tail = node;
    list->size++;
    return true;
}

void *list_peek_head(const list_t *list){
    if (list == NULL || list->head == NULL) return NULL;
    return list->head->value;
}

void *list_peek_tail(const list_t *list){
    if (list == NULL || list->tail == NULL) return NULL;
    return list->tail->value;
}

void *list_pop_head(list_t *list){
    if (list == NULL || list->head == NULL) return NULL;

    node_t* node = list->head->next;
    void* value = list->head->value;

    if (node != NULL) node->prev = NULL; else list->tail = NULL;

    free(list->head);
    list->head = node;

    list->size--;
    return value;
}

void *list_pop_tail(list_t *list){
    if (list == NULL || list->tail == NULL) return NULL;

    node_t* node = list->tail->prev;
    void* value = list->tail->value;

    if (node != NULL) node->next = NULL; else list->head = NULL;

    free(list->tail);
    list->tail = node;

    list->size--;
    return value;
}

void list_destroy(list_t *list, void destroy_value(void *)){
    if (list == NULL) return;

    while (!list_is_empty(list)) {
        void* aux = list_pop_head(list);
        if (destroy_value) destroy_value(aux);
    }
    free(list);
}

list_iter_t *list_iter_create_head(list_t *list){
    if (list == NULL) return NULL;
    
    list_iter_t* iterator = malloc(sizeof(list_iter_t));
    if (iterator == NULL) return NULL;

    iterator->list = list;
    iterator->curr = list->head;

    return iterator;
}

list_iter_t *list_iter_create_tail(list_t *list){
    if (list == NULL) return NULL;

    list_iter_t* iterator = malloc(sizeof(list_iter_t));
    if (iterator == NULL) return NULL;

    iterator->list = list;
    iterator->curr = list->tail;

    return iterator;
}

bool list_iter_forward(list_iter_t *iter){
    if (iter == NULL) return false;
    
    if (iter->curr == NULL || iter->curr->next == NULL) return false;
    iter->curr = iter->curr->next;

    return true;
}

bool list_iter_backward(list_iter_t *iter){
    if (iter == NULL) return false;
    
    if (iter->curr == NULL || iter->curr->prev == NULL) return false;
    iter->curr = iter->curr->prev;

    return true;
}

void *list_iter_peek_current(const list_iter_t *iter){
    if (iter == NULL || iter->curr == NULL) return NULL;
    return iter->curr->value;
}

bool list_iter_at_last(const list_iter_t *iter){
    if (iter == NULL || iter->curr == NULL || iter->list == NULL) return false;
    if (iter->list->size == 0) return true;

    return (iter->curr == iter->list->tail);
}

bool list_iter_at_first(const list_iter_t *iter){
    if (iter == NULL || iter->curr == NULL || iter->list == NULL) return false;
    if (iter->list->size == 0) return true;

    return (iter->curr == iter->list->head);
}

void list_iter_destroy(list_iter_t *iter){
    if (iter == NULL) return;
    free(iter);
}

bool list_iter_insert_after(list_iter_t *iter, void *value){
    return false;
}

bool list_iter_insert_before(list_iter_t *iter, void *value){
    return false;
}

void *list_iter_delete(list_iter_t *iter){
    return NULL;
}