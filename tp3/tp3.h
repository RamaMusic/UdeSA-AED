#include <stdbool.h>
#include <stddef.h>

#ifndef TP3_H
#define TP3_H

struct dictionary;

typedef struct dictionary dictionary_t;
typedef void (*destroy_f)(void *);

typedef struct dictionary_node node;

/* Crea un nuevo diccionario */
dictionary_t *dictionary_create(destroy_f destroy);

/* Inserta un par clave-valor en el diccionario. O(1).
 * Pre-condiciones:
 * - El diccionario existe
 * - La clave tiene largo mayor a cero
 * - El valor puede ser destruido con la función con la que se inicializó el diccionario.
 * Post-condiciones:
 * - Retorna true si se ha podido guardar con éxito el par clave/valor
 * - Retorna false de otro modo.
 * - Si la clave ya estaba presente, se elimina el valor previo
 */
bool dictionary_put(dictionary_t *dictionary, const char *key, void *value);

/* Obtiene un valor del diccionario desde su clave. O(1).
 * Pre-condiciones
 * - El diccionario existe
 * - La clave tiene largo mayor a cero
 * Post-condiciones:
 * - Si la clave está presente, retorna el valor asociado y err debe ser false
 * - De otro modo, debe retornar NULL y err debe ser true
 */
void *dictionary_get(dictionary_t *dictionary, const char *key, bool *err);

/* Elimina una clave del diccionario. O(1).
 * Pre-condiciones
 * - El diccionario existe
 * - La clave tiene largo mayor a cero
 * Retorna true si la clave estaba presente y se pudo eliminar, o false
 * de otro modo.
 */
bool dictionary_delete(dictionary_t *dictionary, const char *key);

/* Elimina una clave y retorna su valor asociado. O(1).
 * Pre-condiciones:
 * - El diccionario existe
 * - La clave tiene largo mayor a cero
 * Post-condiciones:
 * - Si la calve está presente, retorna el valor asocaido y err debe ser false
 * - De otro modo, debe retornar NULL y err debe ser true
 */
void *dictionary_pop(dictionary_t* dictionary, const char *key, bool *err);

/* Indica si hay un valor asociado a la clave indicada. O(1).
 * Pre-condiciones:
 * - El diccionario existe
 * - La clave tiene largo mayor a cero
 * Post-condiciones:
 * - Retorna true si la clave está presente en el diccionario
 * - Retorna false de otro modo
 */
bool dictionary_contains(dictionary_t *dictionary, const char *key);

/* Indica la cantidad de elementos guardados en el diccionario. O(1).
 * Pre-condiciones:
 * - El diccionario existe
 */
size_t dictionary_size(dictionary_t *dictionary);

/* Destruye el diccionario y los valores asociados a todas las claves presentes.
 * Pre-condiciones:
 * - El diccionario existe
 */
void dictionary_destroy(dictionary_t *dictionary);

// Funciones auxiliares

/* Función que calcula el hash de una clave.
 * Pre-condiciones:
 * - La clave tiene largo mayor a cero
 * Post-condiciones:
 * - Retorna el hash de la clave 
*/
unsigned long hash(const char *key);

/* Función que crea un nuevo nodo con la clave y valor indicados. O(1).
 * Pre-condiciones:
 * - La clave tiene largo mayor a cero
 * - El valor puede ser destruido con la función destroy
 * Post-condiciones:
 * - Retorna un nuevo nodo con la clave y valor indicados
*/
node *create_entry(const char *key, void *value);

/* Función que libera la memoria de un nodo.
 * Pre-condiciones:
 * - El nodo existe
 * - El valor puede ser destruido con la función destroy
 * Post-condiciones:
 * - Libera la memoria del nodo y su valor
*/
void free_entry(node *entry, destroy_f destroy);

/* Función que cambia el tamaño del diccionario.
 * Pre-condiciones:
 * - El diccionario existe
 * Post-condiciones:
 * - Retorna true si se ha podido cambiar el tamaño del diccionario
 * - Retorna false de otro modo
*/
bool resize_dictionary(dictionary_t *dictionary);

/* Función que busca un nodo en una lista de nodos.
 * Pre-condiciones:
 * - La lista de nodos existe
 * - La clave tiene largo mayor a cero
 * Post-condiciones:
 * - Retorna el nodo con la clave indicada si se encuentra en la lista
 * - Retorna NULL de otro modo
*/
node *find_entry(dictionary_t *dictionary, const char *key, node **prev);

#endif
