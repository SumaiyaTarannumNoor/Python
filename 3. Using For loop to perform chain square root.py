import cmath
n=3
for i in range(n):
    
    num= eval(input('Enter 10 numbers for chain square root: '))
    num_sqrt=cmath.sqrt(num)
    print('The Square root of {0} is {1:0.3f}+{2:0.3f}j'.format(num, num_sqrt.real, num_sqrt.imag))
        
