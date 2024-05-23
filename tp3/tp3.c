#include <stdlib.h>
#include <string.h>

#include "tp3.h"

#define INITIAL_CAPACITY 16
#define LOAD_FACTOR 0.75

typedef struct dictionary_node {
    char *key;
    void *value;
    struct dictionary_node *next;
} node;

struct dictionary {
    node **container;
    size_t size;
    size_t capacity;
    destroy_f destroy;
};

// Implementación de las funciones principales
dictionary_t *dictionary_create(destroy_f destroy) {
    dictionary_t *dictionary = malloc(sizeof(dictionary_t));
    if (!dictionary) return NULL;

    dictionary->container = calloc(INITIAL_CAPACITY, sizeof(node *));
    if (!dictionary->container) {
        free(dictionary);
        return NULL;
    }

    dictionary->size = 0;
    dictionary->capacity = INITIAL_CAPACITY;
    dictionary->destroy = destroy;

    return dictionary;
};

bool dictionary_put(dictionary_t *dictionary, const char *key, void *value) {
    if (!dictionary || !key) return false;

    node *prev;
    node *entry = find_entry(dictionary, key, &prev);
    // Si la clave ya existe, se reemplaza el valor
    if (entry) {
        if (dictionary->destroy && entry->value)
            dictionary->destroy(entry->value);
        entry->value = value;
        return true;
    }

    entry = create_entry(key, value);
    if (!entry) return false;

    size_t index = hash(key) % dictionary->capacity;
    entry->next = dictionary->container[index];
    dictionary->container[index] = entry;
    dictionary->size++;

    // Si mi tamaño supera el factor de carga, redimensiono al doble
    if ((double)dictionary->size > LOAD_FACTOR * (double)dictionary->capacity) {
        return resize_dictionary(dictionary);
    }

    return true;
};

void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || strlen(key) == 0) {
        if (err) *err = true;
        return NULL;
    }

    node *prev;
    node *entry = find_entry(dictionary, key, &prev);
    if (entry) {
        if (err) *err = false;
        return entry->value;
    }

    if (err) *err = true;
    return NULL;
};

bool dictionary_delete(dictionary_t *dictionary, const char *key) {
    if (!dictionary || !key || strlen(key) == 0) return false;

    node *prev;
    node *entry = find_entry(dictionary, key, &prev);
    if (!entry) return false;

    if (prev) {
        prev->next = entry->next;
    } else {
        size_t index = hash(key) % dictionary->capacity;
        dictionary->container[index] = entry->next;
    }

    free_entry(entry, dictionary->destroy);
    dictionary->size--;
    return true;
};

void *dictionary_pop(dictionary_t *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || strlen(key) == 0) {
        if (err) *err = true;
        return NULL;
    }

    node *prev;
    node *entry = find_entry(dictionary, key, &prev);
    if (!entry) {
        if (err) *err = true;
        return NULL;
    }

    void *value = entry->value;
    if (prev) {
        prev->next = entry->next;
    } else {
        size_t index = hash(key) % dictionary->capacity;
        dictionary->container[index] = entry->next;
    }

    free(entry->key);
    free(entry);
    dictionary->size--;

    if (err) *err = false;
    return value;
};

bool dictionary_contains(dictionary_t *dictionary, const char *key) {
    if (!dictionary || !key || strlen(key) == 0) return false;

    node *prev;
    return find_entry(dictionary, key, &prev) != NULL;
};

size_t dictionary_size(dictionary_t *dictionary) {
    return dictionary ? dictionary->size : 0;
}

void dictionary_destroy(dictionary_t *dictionary) {
    if (!dictionary) return;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        node *entry = dictionary->container[i];
        while (entry) {
            node *next = entry->next;
            free_entry(entry, dictionary->destroy);
            entry = next;
        }
    }

    free(dictionary->container);
    free(dictionary);
};

// Implementación de las funciones auxiliares
unsigned long hash(const char *key) {
    unsigned long hash = 5381;
    int c;
    while ((c = *key++)) hash = ((hash << 5) + hash) + c;
    return hash;
};

node *create_entry(const char *key, void *value) {
    node *entry = malloc(sizeof(node));
    if (!entry) return NULL;

    entry->key = malloc(strlen(key) + 1);
    if (!entry->key) {
        free(entry);
        return NULL;
    }

    strcpy(entry->key, key);
    entry->value = value;
    entry->next = NULL;

    return entry;
};

void free_entry(node *entry, destroy_f destroy) {
    if (entry) {
        free(entry->key);
        if (destroy) destroy(entry->value);
        free(entry);
    }
};

bool resize_dictionary(dictionary_t *dictionary) {
    size_t new_capacity = dictionary->capacity * 2;
    node **new_container = calloc(new_capacity, sizeof(node *));
    if (new_container == NULL) return false;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        node *entry = dictionary->container[i];
        while (entry) {
            size_t new_index = hash(entry->key) % new_capacity;
            node *next_entry = entry->next;
            entry->next = new_container[new_index];
            new_container[new_index] = entry;
            entry = next_entry;
        }
    }

    free(dictionary->container);
    dictionary->container = new_container;
    dictionary->capacity = new_capacity;

    return true;
}

node *find_entry(dictionary_t *dictionary, const char *key, node **prev) {
    size_t index = hash(key) % dictionary->capacity;
    node *entry = dictionary->container[index];
    *prev = NULL;

    while (entry) {
        if (strcmp(entry->key, key) == 0) return entry;
        *prev = entry;
        entry = entry->next;
    }

    return NULL;
}