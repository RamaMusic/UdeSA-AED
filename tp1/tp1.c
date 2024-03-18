#include "tp1.h"
#include <stdlib.h>
#include <math.h>

bool is_prime(int x){
    // Casos base
    if (x <= 1) return false;
    if (x <= 3) return true;
    if (x % 2 == 0 || x % 3 == 0) return false;
    
    // Guardo la raiz cuadrada de x para no calcularla en cada iteracion
    int sqrtX = (int)sqrt(x);

    for (int i = 5; i <= sqrtX; i += 6){
        if (x % i == 0 || x % (i + 2) == 0){
            return false;
        }
    }
    return true;
}

int storage_capacity(float d, float v){
    if (d == 0 || d / v < 0) return 0;
    return (int) (d / v);
}

void swap(int *x, int *y) {

    if (x == NULL || y == NULL) return; // Si alguno de los punteros es NULL, no hago nada.

    int temp = *x;
    *x = *y;
    *y = temp;
    return;
}

int array_max(const int *array, int length) {
    int max = array[0];

    if (length <= 0) return 0;

    for (int i = 1; i < length; i++){
        if (array[i] > max){
            max = array[i];
        }
    }
    return max;
}

void array_map(int *array, int length, int f(int)) {
    if (f == NULL || array == NULL || length <= 0) return; // Si no hay función o el array esta vacío, no hago nada.
    for (int i = 0; i < length; i++){
        array[i] = f(array[i]);
    }
    return;
}

int *copy_array(const int *array, int length) {
    if (array == NULL || length <= 0) return NULL; // Si el array esta vacio lo ignoro.

    int *copy = malloc(length * sizeof(int));
    if (copy == NULL) return NULL; // Si no puedo reservar memoria, devuelvo NULL.

    for (int i = 0; i < length; i++){
        copy[i] = array[i];
    }
    return copy;
}

int **copy_array_of_arrays(const int **array_of_arrays, const int *array_lenghts, int array_amount){
    if (array_of_arrays == NULL || array_lenghts == NULL || array_amount <= 0) return NULL; // Si el array esta vacio, no hago nada.

    int **copy = malloc(array_amount * sizeof(int *));
    if (copy == NULL) return NULL; // Si no puedo reservar memoria, devuelvo NULL.

    for (int i = 0; i < array_amount; i++){
        // Si el array esta vacio, libero la memoria ya reservada y devuelvo NULL.
        if (array_of_arrays[i] == NULL || array_lenghts[i] <= 0) {
             copy[i] = NULL; 
        } else {
            copy[i] = copy_array(array_of_arrays[i], array_lenghts[i]);
            if (copy[i] == NULL) { // Si no puedo reservar memoria, libero lo que reservé y devuelvo NULL.
                for (int j = 0; j < i; j++){
                    free(copy[j]);
                }
                free(copy);
                return NULL;
            }
        }
    }

    return copy; // Devuelvo el array final.
}

void free_array_of_arrays(int **array_of_arrays, int *array_lenghts, int array_amount){
    if (array_of_arrays == NULL || array_lenghts == NULL || array_amount <= 0) { return; } // Si el array está vacio, no hago nada.

    for (int i = 0; i < array_amount; i++){
        if (array_of_arrays[i] != NULL){
            free(array_of_arrays[i]);
        }
    }
    free(array_of_arrays);
    free(array_lenghts);
    return;
}

void bubble_sort(int *array, int length){
    if (array == NULL || length <= 1) { return; } // Si el array es nulo o el largo es 0, no hago nada. Si el largo es 1, ya está ordenada.

    bool swapped = false; // Variable para saber si hubo cambios en la iteración.
    for (int i = 0; i < length-1; i++) {
        swapped = false;
        for (int j = 0; j < length-i-1; j++){
            if (array[j] > array[j+1]) {
                swap(&array[j], &array[j+1]);
                swapped = true;
            }
        }

        // SI no hubo cambios, el array ya está ordenado.
        if (!swapped) return;
    }
    return;
}

bool array_equal(const int *array1, int length1, const int *array2, int length2){
    // Todo esto claramente se puede hacer en un mismo if, pero para facilitar la lectura del código lo voy a separar en casos
    if (array1 == NULL && array2 == NULL) { return true; } // Si ambos arrays son nulos, son iguales.
    if (array1 == NULL || array2 == NULL) { return false; } // Si uno de los arrays es nulo y el otro no, no son iguales.

    if (length1 <= 0 && length2 <= 0) { return true; } // Si ambos arrays están vacíos, son iguales.
    if (length1 <= 0 || length2 <= 0) { return false; } // Si uno de los arrays está vacío y el otro no, no son iguales.
    if (length1 != length2) { return false; } // Si los largos de los arrays son distintos, no son iguales.

    for (int i = 0; i < length1; i++){
        if (array1[i] != array2[i]) { return false; } // Si hay al menos un elemento distinto, los arrays no son iguales.
    }
    return true; // Si llegué hasta acá, los arrays son iguales.
}

bool integer_anagrams(const int *array1, int length1, const int *array2, int length2){
    if (array1 == NULL || array2 == NULL) { return false; } // Si uno de los arrays es nulo y el otro no, no son anagramas.

    if (length1 <= 0 && length2 <= 0) { return true; } // Si ambos arrays están vacíos, son anagramas.
    if (length1 <= 0 || length2 <= 0) { return false; } // Si uno de los arrays está vacío y el otro no, no son anagramas.
    if (length1 != length2) { return false; } // Si los largos de los arrays son distintos, no son anagramas.

    if (array_equal(array1, length1, array2, length2)) { return true; } // Si los arrays son iguales, son anagramas.

    int *copy1 = copy_array(array1, length1);
    int *copy2 = copy_array(array2, length2);

    if (copy1 == NULL || copy2 == NULL) { // Si no puedo reservar memoria, libero lo que reservé y devuelvo false.
        free(copy1);
        free(copy2);
        return false;
    }

    bubble_sort( copy1, length1 );
    bubble_sort( copy2, length2 );

    bool result = array_equal( copy1, length1, copy2, length2 );

    free( copy1 );
    free( copy2 );

    return result;

    // Alternativa con menos allocs y a su vez con menor complejidad temporal (O(n^2) vs O(3*n^2) pero sin codigo repetido:
    //     int obj, count1, count2;

    //     for (int i = 0; i < length1; i++) {
    //         obj = array1[i];
    //         count1 = 0;
    //         count2 = 0;

    //         for (int j = 0; j < length1; j++) {
    //             if (array1[j] == obj) count1++;
    //             if (array2[j] == obj) count2++;
    //         }

    //         if (count1 != count2) return false;
    //     }

    //     return true;
}