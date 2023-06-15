t = int(input()) 
for i in range (0,t): 
    N = int(input()) 
    A = list(map(int, input().split())) 
    k = int(input()) 
    result = A[k-1]
    A = sorted(A) 
    for i in range(0, len(A)):
        if A[i] == result: 
            print(i+1)            
            
            