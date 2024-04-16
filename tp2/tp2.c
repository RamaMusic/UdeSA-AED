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

    return list_length(list) == 0;
}

bool list_insert_head(list_t *list, void *value){
    return list_insert_end(list, value, true);
}

bool list_insert_tail(list_t *list, void *value){
    return list_insert_end(list, value, false);
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
    return list_pop_end(list, true);
}

void *list_pop_tail(list_t *list){
    return list_pop_end(list, false);
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
    return create_iter_at_end(list, true);
}

list_iter_t *list_iter_create_tail(list_t *list){
    return create_iter_at_end(list, false);
}

bool list_iter_forward(list_iter_t *iter){
    return list_iter_move(iter, true);
}

bool list_iter_backward(list_iter_t *iter){
    return list_iter_move(iter, false);
}

void *list_iter_peek_current(const list_iter_t *iter){
    if (iter == NULL || iter->curr == NULL) return NULL;

    return iter->curr->value;
}

bool list_iter_at_first(const list_iter_t *iter){
    return is_iter_at(iter, true);
}

bool list_iter_at_last(const list_iter_t *iter){
    return is_iter_at(iter, false);
}

void list_iter_destroy(list_iter_t *iter){
    if (iter == NULL) return;
    free(iter);
}

bool list_iter_insert_after(list_iter_t *iter, void *value){
    return list_iter_insert_at(iter, value, true);
}


bool list_iter_insert_before(list_iter_t *iter, void *value){
    return list_iter_insert_at(iter, value, false);
}

void *list_iter_delete(list_iter_t *iter){
    if (iter == NULL || iter->list == NULL || iter->curr == NULL) return false;

    if (list_iter_at_first(iter)) {
        list_iter_forward(iter);
        return list_pop_head(iter->list);
    }
    if (list_iter_at_last(iter)) {
        list_iter_backward(iter);
        return list_pop_tail(iter->list);
    }

    void* value = list_iter_peek_current(iter);
    node_t* node = iter->curr;

    node->next->prev = node->prev;
    node->prev->next = node->next;

    iter->curr = node->next;
    free(node);
    
    iter->list->size--;
    return value;
}

/*    ____          _                       __                  _   _                 
     / ___|   _ ___| |_ ___  _ __ ___      / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
    | |  | | | / __| __/ _ \| '_ ` _ \    | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
    | |__| |_| \__ \ || (_) | | | | | |   |  _| |_| | | | | (__| |_| | (_) | | | \__ \
     \____\__,_|___/\__\___/|_| |_| |_|   |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
*/

void insert_node(list_t *list, node_t *node, node_t *prev, node_t* next) {
    node->next = next;
    node->prev = prev;

    if (prev != NULL) prev->next = node; else list->head = node;
    if (next != NULL) next->prev = node; else list->tail = node;

    list->size++;
}

void *remove_node(list_t *list, bool head) {
    node_t* node = head ? list->head->next : list->tail->prev;
    void* value = head ? list->head->value : list->tail->value;

    if (node != NULL) {
        if (head) node->prev = NULL; else node->next = NULL;
    } else {
        if (head) list->tail = NULL; else list->head = NULL;
    }

    free(head ? list->head : list->tail);
    if (head) list->head = node; else list->tail = node;

    list->size--;
    return value;
}

bool list_insert_end(list_t *list, void *value, bool head){
    if (list == NULL) return false;

    node_t* node = malloc(sizeof(node_t));
    if (node == NULL) return false;

    node_t* prev = head ? NULL : list->tail;
    node_t* next = head ? list->head : NULL;

    node->value = value;
    insert_node(list, node, prev, next);

    return true;
}

void *list_pop_end(list_t *list, bool head){
    if (list == NULL || list->head == NULL || list->tail == NULL) return NULL;

    return remove_node(list, head);
}

list_iter_t *create_iter_at_end(list_t *list, bool head){
    if (list == NULL) return NULL;

    list_iter_t* iterator = malloc(sizeof(list_iter_t));
    if (iterator == NULL) return NULL;

    iterator->list = list;
    iterator->curr = head ? list->head : list->tail;

    return iterator;
}

bool list_iter_move(list_iter_t *iter, bool forward){
    if (iter == NULL || iter->curr == NULL) return false;

    node_t* next = forward ? iter->curr->next : iter->curr->prev;

    if (next == NULL) return false;
    iter->curr = next;

    return true;
}

bool is_iter_at(const list_iter_t *iter, bool head){
    if (iter == NULL || iter->list == NULL) return false;

    node_t* node = head ? iter->list->head : iter->list->tail;
    return node == iter->curr;
}

bool list_iter_insert_at(list_iter_t *iter, void *value, bool after){
    if (iter == NULL || iter->list == NULL) return false;

    if (list_is_empty(iter->list)) {
        bool result = list_insert_head(iter->list, value);
        iter->curr = iter->list->head;
        return result;
    }

    if (after ? list_iter_at_last(iter) : list_iter_at_first(iter)) {
        return after ? list_insert_tail(iter->list, value) : list_insert_head(iter->list, value);
    }

    node_t* node = malloc(sizeof(node_t));
    if (node == NULL) return false;

    node->value = value;
    node->prev = after ? iter->curr : iter->curr->prev;
    node->next = after ? iter->curr->next : iter->curr;

    if (after) {
        if (node->next != NULL) node->next->prev = node;
        iter->curr->next = node;
    } else {
        if (node->prev != NULL) node->prev->next = node; else iter->list->head = node;
        iter->curr->prev = node;
    }

    iter->list->size++;
    return true;
}