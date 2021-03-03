import cmath

Number=eval(input('Enter the complex number: '))
SQRT= cmath.sqrt(Number)
print('The square root of {0} is {1:0.3f}+{2:0.3f}j'.format(Number,SQRT.real,SQRT.imag))
