#include "tp1.h"
#include <stdlib.h>
#include <math.h>

bool is_prime(int x){
    for (int i = 2; i <= sqrt(x); i++){
        if (x % i == 0){
            return false;
        }
    }
    return true;
}

int storage_capacity(float d, float v){
    if (d == 0) { return 0; }

    float result = d / v;
    if (result < 0) { return 0; }
    return (int) result;
}

void swap(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
    return;
}

int array_max(const int *array, int length) {
    int max = array[0];
    for (int i = 1; i < length; i++){
        if (array[i] > max){
            max = array[i];
        }
    }
    return max;
}

void array_map(int *array, int length, int f(int)) {
    if (f == NULL) { return; }
    for (int i = 0; i < length; i++){
        array[i] = f(array[i]);
    }
    return;
}

int *copy_array(const int *array, int length) {
    return NULL;
}

int **copy_array_of_arrays(const int **array_of_arrays, const int *array_lenghts, int array_amount){
    return NULL;
}

void free_array_of_arrays(int **array_of_arrays, int *array_lenghts, int array_amount){
    return;
}

void bubble_sort(int *array, int length){
    return;
}

bool array_equal(const int *array1, int length1, const int *array2, int length2){
    return true;
}

bool integer_anagrams(const int *array1, int length1,
                      const int *array2, int length2){
    return true;
}