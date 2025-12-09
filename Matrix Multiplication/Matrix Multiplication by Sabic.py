import numpy as np
import time

rows = 256   # Change to 16, 32, 64, 128 as needed
columns = 256

A = []
B = []

print("Enter the elements for first Matrix:\n")
for i in range(rows):
    n = []
    for j in range(columns):
        number = input()
        if number != ' ':
            n.append(int(number))
    A.append(n)

print("Enter the elements for second Matrix:\n")
for i in range(rows):
    n = []
    for j in range(columns):
        number = input()
        if number != ' ':
            n.append(int(number))
    B.append(n)

A = np.array(A)
B = np.array(B)

begin = time.time()
C = np.matmul(A, B)
end = time.time()

print("The Product of the Matrices is:\n")
print(C)

print("Matrix Multiplication run time:", end - begin)
