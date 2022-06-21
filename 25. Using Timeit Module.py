import numpy as np
from timeit import default_timer as timer

rows = 256
columns = 256

A=[]
B=[]

for i in range(rows):
    n=[]
    for j in range(columns):
        number = input()
        if number!=' ':
            n.append(int(number))
    A.append(n)        

for i in range(rows):
    n=[]
    for j in range(columns):
        number = input()
        if number!=' ':
            n.append(int(number))
    B.append(n)        


A= np.array(A)
B= np.array(B)
begin=timer()
C= np.matmul(A,B)
end=timer()
print(C)
print(end-begin)
