#include "tp3.h"

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

struct entry {
    bool is_occupied;
    bool is_deleted;
    char *key;
    void *value;
};

struct dictionary {
    struct entry *table;
    size_t capacity;
    size_t size;
    float growth_threshold;
    float growth_factor;
    destroy_f destroy;
};

static inline uint32_t hash(const char *key, size_t count) {
    uint32_t h = 0x811c9dc5;
    for (size_t i = 0; i < count; i++) {
        h = (h ^ key[i]) * 0x01000193;
    }
    return h;
}

static char *copy_string(const char *src) {
    size_t len = strlen(src) + 1;
    char *dst = malloc(len);
    if (dst) {
        memcpy(dst, src, len);
    }
    return dst;
}

static struct entry *find_entry_internal(struct dictionary *dictionary, const char *key, bool allocate_if_not_found) {
    if (!dictionary || !key) return NULL;
    
    uint32_t hash_value = hash(key, strlen(key));
    unsigned long index = hash_value % dictionary->capacity;
    unsigned long original_index = index;
    unsigned long i = 1;
    struct entry *free_entry = NULL;

    while (dictionary->table[index].is_occupied) {
        if (!dictionary->table[index].is_deleted && strcmp(dictionary->table[index].key, key) == 0) {
            return &dictionary->table[index];
        }
        if (dictionary->table[index].is_deleted && free_entry == NULL) {
            free_entry = &dictionary->table[index];
        }
        index = (original_index + i * i) % dictionary->capacity;
        i++;
    }

    return allocate_if_not_found ? (free_entry ? free_entry : &dictionary->table[index]) : NULL;
}


static bool resize_dictionary(struct dictionary *dictionary) {
    if (!dictionary) return false;

    size_t new_capacity = (size_t)((float)dictionary->capacity * dictionary->growth_factor);
    if (new_capacity <= dictionary->capacity) return false;

    struct entry *new_table = calloc(new_capacity, sizeof(struct entry));
    if (!new_table) return false;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        struct entry old_entry = dictionary->table[i];
        if (old_entry.is_occupied && !old_entry.is_deleted) {
            uint32_t hash_value = hash(old_entry.key, strlen(old_entry.key));
            unsigned long index = hash_value % new_capacity;
            unsigned long original_index = index;
            unsigned long j = 1;
            while (new_table[index].is_occupied) {
                index = (original_index + j * j) % new_capacity;
                j++;
            }
            new_table[index] = old_entry;
        }
    }

    free(dictionary->table);
    dictionary->table = new_table;
    dictionary->capacity = new_capacity;
    return true;
}


struct dictionary *dictionary_create(destroy_f destroy) {
    struct dictionary *dic = malloc(sizeof(struct dictionary));
    if (!dic) return NULL;

    dic->capacity = 256;
    dic->size = 0;
    dic->growth_threshold = 0.75;
    dic->growth_factor = 2.0;
    dic->destroy = destroy;

    dic->table = calloc(dic->capacity, sizeof(struct entry));
    if (!dic->table) {
        free(dic);
        return NULL;
    }

    return dic;
}

bool dictionary_put(struct dictionary *dictionary, const char *key, void *value) {
    if (!dictionary || !key || !dictionary->capacity) return false;

    if (dictionary->size >= (size_t)((double)dictionary->capacity * dictionary->growth_threshold)) {
        if (!resize_dictionary(dictionary)) return false;
    }

    struct entry *entry = find_entry_internal(dictionary, key, true);
    if (!entry) return false;

    if (!entry->is_occupied || entry->is_deleted) {
        char *new_key = copy_string(key);
        if (!new_key) return false;

        entry->key = new_key;
        entry->is_occupied = true;
        entry->is_deleted = false;
        dictionary->size++;
    } else if (dictionary->destroy) {
        dictionary->destroy(entry->value);
    }

    entry->value = value;
    return true;
}

void *dictionary_get(struct dictionary *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || !dictionary->capacity) {
        if (err) *err = true;
        return NULL;
    }

    struct entry *entry = find_entry_internal(dictionary, key, false);
    if (!entry || entry->is_deleted) {
        if (err) *err = true;
        return NULL;
    }

    if (err) *err = false;
    return entry->value;
}

bool dictionary_delete(struct dictionary *dictionary, const char *key) {
    if (!dictionary || !key || !dictionary->capacity) return false;

    bool err;
    void *value = dictionary_pop(dictionary, key, &err);
    if (err) return false;

    if (dictionary->destroy) {
        dictionary->destroy(value);
    }

    return true;
}

void *dictionary_pop(struct dictionary *dictionary, const char *key, bool *err) {
    if (!dictionary || !key || !dictionary->capacity) {
        if (err) *err = true;
        return NULL;
    }

    struct entry *entry = find_entry_internal(dictionary, key, false);
    if (!entry || !entry->is_occupied || entry->is_deleted) {
        if (err) *err = true;
        return NULL;
    }

    void *value = entry->value;
    free(entry->key);
    entry->is_deleted = true;
    dictionary->size--;
    if (err) *err = false;
    return value;
}

bool dictionary_contains(struct dictionary *dictionary, const char *key) {
    if (!dictionary || !key) return false;
    struct entry *entry = find_entry_internal(dictionary, key, false);
    return entry != NULL && entry->is_occupied && !entry->is_deleted;
}

size_t dictionary_size(struct dictionary *dictionary) {
    if (!dictionary) return 0;
    return dictionary->size;
}

void dictionary_destroy(struct dictionary *dictionary) {
    if (!dictionary) return;

    for (size_t i = 0; i < dictionary->capacity; i++) {
        if (dictionary->table[i].is_occupied && !dictionary->table[i].is_deleted) {
            if (dictionary->destroy) {
                dictionary->destroy(dictionary->table[i].value);
            }
            free(dictionary->table[i].key);
        }
    }
    free(dictionary->table);
    free(dictionary);
}
