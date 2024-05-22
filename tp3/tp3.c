#include "tp3.h"
#include <stdlib.h>
#include <string.h>

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

void resize_dictionary(dictionary_t *dictionary);

unsigned long hash(const char *key) {
  unsigned long hash = 5381;
  int c;
  while ((c = *key++)) hash = ((hash << 5) + hash) + c;
  return hash;
};

void free_entry(node *entry, destroy_f destroy) {
  if (entry) {
    free(entry->key);
    if (destroy) destroy(entry->value);
    free(entry);
  }
};

node *create_entry(const char *key, void *value) {
  node *entry = malloc(sizeof(node));
  if (!entry) return NULL;

  entry->key = malloc(strlen(key) + 1);  // Asignar memoria para la clave
  if (!entry->key) {
    free(entry);
    return NULL;
  }

  strcpy(entry->key, key);

  entry->value = value;
  entry->next = NULL;

  return entry;
};

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
  if (!dictionary || !key) return false;  // Removed || !value

  size_t index = hash(key) % dictionary->capacity;

  node *entry = dictionary->container[index];
  while (entry) {
    if (strcmp(entry->key, key) == 0) {
      if (dictionary->destroy && entry->value) dictionary->destroy(entry->value);  // Added && entry->value
      entry->value = value;
      return true;
    }
    entry = entry->next;
  }

  node *new_entry = create_entry(key, value);
  if (!new_entry) return false;

  if (dictionary->container[index]) {
    new_entry->next = dictionary->container[index];
  }

  dictionary->container[index] = new_entry;
  dictionary->size++;
  // Redimensionar si el factor de carga > LOAD_FACTOR
  if ((double)dictionary->size > LOAD_FACTOR * (double)dictionary->capacity) {
    resize_dictionary(dictionary);
  }

  return true;
};

void resize_dictionary(dictionary_t *dictionary) {
  size_t new_capacity = dictionary->capacity * 2;
  node **new_container = calloc(new_capacity, sizeof(node *));
  
  // Rehash todas las entradas
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
}

void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err) {
  if (!dictionary || !key || strlen(key) == 0) {
    if (err) *err = true;
    return NULL;
  }

  size_t index = hash(key) % dictionary->capacity;
  node *entry = dictionary->container[index];

  while (entry) {
    if (strcmp(entry->key, key) == 0) {
      if (err) *err = false;
      return entry->value;
    }
    entry = entry->next;
  }

  if (err) *err = true;
  return NULL;
};

bool dictionary_delete(dictionary_t *dictionary, const char *key) {
  if (!dictionary || !key || strlen(key) == 0) return false;

  size_t index = hash(key) % dictionary->capacity;
  node *entry = dictionary->container[index];
  node *prev = NULL;

  while (entry) {
    if (strcmp(entry->key, key) == 0) {
      if (prev) {
        prev->next = entry->next;
      } else {
        dictionary->container[index] = entry->next;
      }
      
      // Liberar la memoria de entry sólo después de haber actualizado todas las referencias a ella
      free_entry(entry, dictionary->destroy);
      
      dictionary->size--;
      return true;
    }
    prev = entry;
    entry = entry->next;
  }

  return false;
};

void *dictionary_pop(dictionary_t *dictionary, const char *key, bool *err) {
  if (!dictionary || !key || strlen(key) == 0) {
    if (err) *err = true;
    return NULL;
  }

  size_t index = hash(key) % dictionary->capacity;
  node *entry = dictionary->container[index];
  node *prev = NULL;

  while (entry) {
    if (strcmp(entry->key, key) == 0) {
      void *value = entry->value; // Save the value before freeing the entry
      if (prev) {
        prev->next = entry->next;
      } else {
        dictionary->container[index] = entry->next;
      }
      free(entry->key); // Free the key
      free(entry); // Free the entry, but not the value
      dictionary->size--;
      if (err) *err = false;
      return value; // Return the saved value
    }
    prev = entry;
    entry = entry->next;
  }

  if (err) *err = true;
  return NULL;
};
bool dictionary_contains(dictionary_t *dictionary, const char *key) {
  if (!dictionary || !key || strlen(key) == 0) return false;

  size_t index = hash(key) % dictionary->capacity;
  node *entry = dictionary->container[index];

  while (entry) {
    if (strcmp(entry->key, key) == 0) return true;
    entry = entry->next;
  }

  return false;
};

size_t dictionary_size(dictionary_t *dictionary) {
  if (!dictionary) return 0;

  return dictionary->size;
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
