import numpy as np
import time

A=[[2, 4, 9, 678],
  [3, 2, 9, 284]]
B = [[1, 4, 50004],
     [3, 6, 70009],
     [9, 8, 90007],
     [125, 246, 120008]]

A= np.array(A)
B= np.array(B)
begin=time.time()
C= np.matmul(A,B)
end=time.time()
print(C)
print(end-begin)
