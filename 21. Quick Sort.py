def partition (array, low, high):
    pivot = array[high]
    i = low -1
    #compare
    for j in range (low, high):
        if array [j]<= pivot:
            i = i+1
            #swap
            (array[i],array[j])= (array[j],array[i])

     #pivot element swap
    (array[i+1],array[high]) = (array[high], array[i+1])
    return i+1


def quickSort(array, low, high):
    if low < high:
     pi = partition (array, low, high)

     quickSort(array, low, pi-1)

     quickSort(array, pi +1, high)

data = list(map(int,input().split())) 
print("Unsorted array" , data)
#print(data)

size = len(data)

quickSort(data, 0, size-1)

print('Sorted Array in Ascending order:')
print(data)
    

