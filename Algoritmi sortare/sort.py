import random
import time
import numpy as np


# Generare 1.000 de liste cu dimensiuni aleatorii între 10.000 și 100.000
def generate_integer_lists(num_lists):
    lists = []
    for _ in range(num_lists):
        list_length = random.randrange(10_000, 100_000)
        curr_list = [random.randint(0, 1_000_000) for _ in range(list_length)]  # Integers within a large range
        lists.append(curr_list)
    return lists

# Algoritmi de sortare
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


# Compararea performanței
def benchmark_sorting_algorithms(lists, algorithms):
    results = {alg.__name__: [] for alg in algorithms}
   
    for alg in algorithms:
        print(alg)
        for lst in lists:
            lst_copy = lst[:]  # Copie pentru a păstra lista inițială
            start_time = time.time()
            if alg.__name__ == "quick_sort":
                sorted_lst = alg(lst_copy)  # Quick Sort returnează o listă nouă
            else:
                
                alg(lst_copy)  # Alți algoritmi sortează în loc
            end_time = time.time()
            results[alg.__name__].append(end_time - start_time)
    
    return results

def counting_sort(arr, max_value=None):
    """Counting sort for non-negative integers."""
    if max_value is None:
        max_value = max(arr)
    
    count = [0] * (max_value + 1)
    output = [0] * len(arr)

    # Count occurrences
    for num in arr:
        count[num] += 1

    # Update count array to store positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build the output array
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    # Copy sorted array back to original
    for i in range(len(arr)):
        arr[i] = output[i]

def radix_sort(arr):
    """Radix sort using Counting Sort as a subroutine."""
    if len(arr) == 0:
        return

    # Find the maximum number to determine the number of digits
    max_val = max(arr)

    # Apply counting sort for each digit
    exp = 1
    while max_val // exp > 0:
        counting_sort_radix(arr, exp)
        exp *= 10


def counting_sort_radix(arr, exp):
    """Counting sort used by Radix Sort."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Digits 0-9

    # Count occurrences of each digit
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # Update count array to store positions
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copy sorted array back to original
    for i in range(n):
        arr[i] = output[i]
# Generare și benchmark
nr_liste = 1000 # Începe cu 10 liste pentru testare; extinde la 1.000 ulterior
lists = generate_integer_lists(nr_liste)

algorithms = [counting_sort, radix_sort, merge_sort, quick_sort, heap_sort]
results = benchmark_sorting_algorithms(lists, algorithms)

# Calculare medii și afișare rezultate
for alg, times in results.items():
    print(f"{alg}: Average time = {np.mean(times):.4f} seconds")
