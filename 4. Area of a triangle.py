#a = 5
#b = 6
#c = 7
a = float(input('Enter first side of the triangel: '))
b = float(input('Enter second side of the triangel: '))
c = float(input('Enter third side of the triangel: '))

s = (a+b+c) / 2

area = (s*(s-a)*(s-b)*(s-c)) ** 0.5

print('The area of the triangle is %0.2f '%area)
