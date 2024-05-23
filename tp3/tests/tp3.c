#include "tp3.h"
#include <stdlib.h>
#include <string.h>

// Estructura para un nodo de la tabla hash
typedef struct node {
    char *key;
    void *value;
    struct node *next;
} node_t;

// Estructura para el diccionario
struct dictionary {
    destroy_f destroy;
    size_t size;
    node_t **buckets;
    size_t capacity;
};

// Función auxiliar para crear un nodo
static node_t *create_node(const char *key, void *value) {
    node_t *new_node = malloc(sizeof(node_t));
    if (new_node == NULL) {
        return NULL;
    }
    new_node->key = strcpy(malloc(strlen(key) + 1), key);
    new_node->value = value;
    new_node->next = NULL;
    return new_node;
}

// Función auxiliar para liberar un nodo
static void destroy_node(node_t *node, destroy_f destroy) {
    if (node == NULL) {
        return;
    }
    if (destroy != NULL && node->value != NULL) {
        destroy(node->value);
    }
    free(node->key);  // Free the key here
    free(node);
}

// Función auxiliar para buscar un nodo en la lista
static node_t *find_node(node_t *list, const char *key) {
    node_t *current = list;
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

// Función auxiliar para eliminar un nodo de la lista
static void remove_node(node_t **list_ptr, const char *key, destroy_f destroy) {
    node_t *current = *list_ptr;
    node_t *prev = NULL;

    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            if (prev == NULL) {
                *list_ptr = current->next;
            } else {
                prev->next = current->next;
            }
            destroy_node(current, destroy);
            return;
        }
        prev = current;
        current = current->next;
    }
}

// Función para crear un nuevo diccionario
dictionary_t *dictionary_create(destroy_f destroy) {
    dictionary_t *dict = malloc(sizeof(dictionary_t));
    if (dict == NULL) {
        return NULL;
    }

    dict->destroy = destroy;
    dict->size = 0;
    dict->capacity = 10;  // Tamaño inicial de la tabla hash
    dict->buckets = calloc(dict->capacity, sizeof(node_t *));
    if (dict->buckets == NULL) {
        free(dict);
        return NULL;
    }

    return dict;
}

// Función hash básica para obtener el índice
static size_t hash(const char *key, size_t capacity) {
    size_t hashval = 0;
    for (size_t i = 0; key[i] != '\0'; i++) {
        hashval = key[i] + 31 * hashval;
    }
    return hashval % capacity;
}

// Función para redimensionar la tabla hash si es necesario
static void resize(dictionary_t *dictionary) {
    size_t new_capacity = dictionary->capacity * 2;
    node_t **new_buckets = calloc(new_capacity, sizeof(node_t *));
    if (new_buckets == NULL) {
        return;
    }

    // Rehashing de todos los elementos
    for (size_t i = 0; i < dictionary->capacity; i++) {
        node_t *current = dictionary->buckets[i];
        while (current != NULL) {
            node_t *next = current->next;
            size_t index = hash(current->key, new_capacity);
            current->next = new_buckets[index];
            new_buckets[index] = current;
            current = next;
        }
    }

    // Liberar la tabla hash anterior
    free(dictionary->buckets);

    dictionary->buckets = new_buckets;
    dictionary->capacity = new_capacity;
}

// Función para insertar un par clave-valor en el diccionario
bool dictionary_put(dictionary_t *dictionary, const char *key, void *value) {
    if (dictionary == NULL || key == NULL) {
        return false;
    }

    // Obtener el índice usando la función hash
    size_t index = hash(key, dictionary->capacity);

    // Buscar si la clave ya existe
    node_t *existing_node = find_node(dictionary->buckets[index], key);
    if (existing_node != NULL) {
        // Si la clave existe, eliminar el valor actual
        if (dictionary->destroy != NULL && existing_node->value != NULL) {
            dictionary->destroy(existing_node->value);
        }
        existing_node->value = value;
        return true;
    }

    // Crear un nuevo nodo
    node_t *new_node = create_node(key, value);
    if (new_node == NULL) {
        return false;
    }

    // Insertar el nuevo nodo al inicio de la lista
    new_node->next = dictionary->buckets[index];
    dictionary->buckets[index] = new_node;
    dictionary->size++;

    // Redimensionar si la carga excede cierto factor de carga (ej. 0.75)
    if ((double) dictionary->size / (double) dictionary->capacity >= 0.75) {
        resize(dictionary);
    }

    return true;
}

// Función para obtener un valor del diccionario desde su clave
void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err) {
    if (dictionary == NULL || key == NULL || err == NULL) {
        if (err != NULL) {
            *err = true;
        }
        return NULL;
    }

    // Obtener el índice usando la función hash
    size_t index = hash(key, dictionary->capacity);

    // Buscar el nodo en la lista correspondiente
    node_t *node = find_node(dictionary->buckets[index], key);
    if (node == NULL) {
        *err = true;
        return NULL;
    }

    *err = false;
    return node->value;
}

// Función para eliminar una clave del diccionario
bool dictionary_delete(dictionary_t *dictionary, const char *key) {
    if (dictionary == NULL || key == NULL) {
        return false;
    }

    // Obtener el índice usando la función hash
    size_t index = hash(key, dictionary->capacity);

    // Buscar y eliminar el nodo de la lista
    remove_node(&dictionary->buckets[index], key, dictionary->destroy);
    dictionary->size--;

    return true;
}

// Función para eliminar una clave y retornar su valor asociado
void *dictionary_pop(dictionary_t *dictionary, const char *key, bool *err) {
    if (dictionary == NULL || key == NULL || err == NULL) {
        if (err != NULL) {
            *err = true;
        }
        return NULL;
    }

    // Obtener el índice usando la función hash
    size_t index = hash(key, dictionary->capacity);

    // Buscar y eliminar el nodo de la lista
    node_t *node = find_node(dictionary->buckets[index], key);
    if (node == NULL) {
        *err = true;
        return NULL;
    }

    // Remover el nodo de la lista
    if (node == dictionary->buckets[index]) {
        dictionary->buckets[index] = node->next;
    } else {
        remove_node(&dictionary->buckets[index], key, dictionary->destroy);
    }
    void *value = node->value;
    free(node->key);
    free(node);
    dictionary->size--;
    *err = false;
    return value;
}

// Función para verificar si una clave está presente en el diccionario
bool dictionary_contains(dictionary_t *dictionary, const char *key) {
    if (dictionary == NULL || key == NULL) {
        return false;
    }

    // Obtener el índice usando la función hash
    size_t index = hash(key, dictionary->capacity);

    // Buscar si la clave existe en la lista correspondiente
    return find_node(dictionary->buckets[index], key) != NULL;
}

// Función para obtener la cantidad de elementos en el diccionario
size_t dictionary_size(dictionary_t *dictionary) {
    if (dictionary == NULL) {
        return 0;
    }

    return dictionary->size;
}

// Función para destruir el diccionario y liberar la memoria
void dictionary_destroy(dictionary_t *dictionary) {
    if (dictionary == NULL) {
        return;
    }

    // Liberar todos los nodos de la tabla hash
    for (size_t i = 0; i < dictionary->capacity; i++) {
        node_t *current = dictionary->buckets[i];
        while (current != NULL) {
            node_t *next = current->next;
            destroy_node(current, dictionary->destroy);
            current = next;
        }
    }

    // Liberar la tabla hash y la estructura del diccionario
    free(dictionary->buckets);
    free(dictionary);
}