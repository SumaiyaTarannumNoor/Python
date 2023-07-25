pos = -1

def search(list, n):

    lower = 0
    upper = len(list) - 1

    while lower <= upper:
        mid = (lower+upper) // 2

        if list[mid] == n:
            globals()['pos'] = mid
            return True

        else:
            if list[mid] < n:
                lower = mid
            else:
                upper = mid

list = [4, 45, 78, 1000, 30006, 400067]

n = 4

if search(list, n):
    print("Found at: ", pos+1)
else:
    print("Not Found")