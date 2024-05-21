#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>
#include <string.h>
#include "tp3.h"


#define INITIAL_CAPACITY 16
#define LOAD_FACTOR 0.75

typedef struct dictionary_entry {
    char *key;
    void *value;
    struct dictionary_entry *next;
} dictionary_entry_t;

struct dictionary {
    dictionary_entry_t **buckets;
    size_t size;
    size_t capacity;
    destroy_f destroy;
};

static size_t hash(const char *key) {
    size_t hash = 5381;
    int c;
    while ((c = *key++))
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    return hash;
}

static dictionary_entry_t *create_entry(const char *key, void *value) {
    dictionary_entry_t *entry = malloc(sizeof(dictionary_entry_t));
    if (!entry) return NULL;
    entry->key = strdup(key);
    if (!entry->key) {
        free(entry);
        return NULL;
    }
    entry->value = value;
    entry->next = NULL;
    return entry;
}

static void free_entry(dictionary_entry_t *entry, destroy_f destroy) {
    if (entry) {
        free(entry->key);
        if (destroy) destroy(entry->value);
        free(entry);
    }
}

static void resize(dictionary_t *dictionary) {
    size_t new_capacity = dictionary->capacity * 2;
    dictionary_entry_t **new_buckets = calloc(new_capacity, sizeof(dictionary_entry_t *));
    if (!new_buckets) return;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        dictionary_entry_t *entry = dictionary->buckets[i];
        while (entry) {
            dictionary_entry_t *next = entry->next;
            size_t index = hash(entry->key) % new_capacity;
            entry->next = new_buckets[index];
            new_buckets[index] = entry;
            entry = next;
        }
    }

    free(dictionary->buckets);
    dictionary->buckets = new_buckets;
    dictionary->capacity = new_capacity;
}

dictionary_t *dictionary_create(destroy_f destroy) {
    dictionary_t *dictionary = malloc(sizeof(dictionary_t));
    if (!dictionary) return NULL;

    dictionary->buckets = calloc(INITIAL_CAPACITY, sizeof(dictionary_entry_t *));
    if (!dictionary->buckets) {
        free(dictionary);
        return NULL;
    }

    dictionary->size = 0;
    dictionary->capacity = INITIAL_CAPACITY;
    dictionary->destroy = destroy;

    return dictionary;
}

bool dictionary_put(dictionary_t *dictionary, const char *key, void *value) {
    if (!dictionary || !key || strlen(key) == 0) return false;

    if (dictionary->size >= (size_t)((double)dictionary->capacity * LOAD_FACTOR)) {
        resize(dictionary);
    }

    size_t index = hash(key) % dictionary->capacity;
    dictionary_entry_t *entry = dictionary->buckets[index];
    dictionary_entry_t *prev = NULL;

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            if (dictionary->destroy) dictionary->destroy(entry->value);
            entry->value = value;
            return true;
        }
        prev = entry;
        entry = entry->next;
    }

    dictionary_entry_t *new_entry = create_entry(key, value);
    if (!new_entry) return false;

    if (prev) {
        prev->next = new_entry;
    } else {
        dictionary->buckets[index] = new_entry;
    }
    dictionary->size++;
    return true;
}

void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || strlen(key) == 0) {
        if (err) *err = true;
        return NULL;
    }

    size_t index = hash(key) % dictionary->capacity;
    dictionary_entry_t *entry = dictionary->buckets[index];

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            if (err) *err = false;
            return entry->value;
        }
        entry = entry->next;
    }

    if (err) *err = true;
    return NULL;
}

bool dictionary_delete(dictionary_t *dictionary, const char *key) {
    if (!dictionary || !key || strlen(key) == 0) return false;

    size_t index = hash(key) % dictionary->capacity;
    dictionary_entry_t *entry = dictionary->buckets[index];
    dictionary_entry_t *prev = NULL;

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            if (prev) {
                prev->next = entry->next;
            } else {
                dictionary->buckets[index] = entry->next;
            }
            free_entry(entry, dictionary->destroy);
            dictionary->size--;
            return true;
        }
        prev = entry;
        entry = entry->next;
    }

    return false;
}

void *dictionary_pop(dictionary_t *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || strlen(key) == 0) {
        if (err) *err = true;
        return NULL;
    }

    size_t index = hash(key) % dictionary->capacity;
    dictionary_entry_t *entry = dictionary->buckets[index];
    dictionary_entry_t *prev = NULL;

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            void *value = entry->value;
            if (prev) {
                prev->next = entry->next;
            } else {
                dictionary->buckets[index] = entry->next;
            }
            free(entry->key);
            free(entry);
            dictionary->size--;
            if (err) *err = false;
            return value;
        }
        prev = entry;
        entry = entry->next;
    }

    if (err) *err = true;
    return NULL;
}

bool dictionary_contains(dictionary_t *dictionary, const char *key) {
    if (!dictionary || !key || strlen(key) == 0) return false;

    size_t index = hash(key) % dictionary->capacity;
    dictionary_entry_t *entry = dictionary->buckets[index];

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return true;
        }
        entry = entry->next;
    }

    return false;
}

size_t dictionary_size(dictionary_t *dictionary) {
    return dictionary ? dictionary->size : 0;
}

void dictionary_destroy(dictionary_t *dictionary) {
    if (!dictionary) return;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        dictionary_entry_t *entry = dictionary->buckets[i];
        while (entry) {
            dictionary_entry_t *next = entry->next;
            free_entry(entry, dictionary->destroy);
            entry = next;
        }
    }

    free(dictionary->buckets);
    free(dictionary);
}
