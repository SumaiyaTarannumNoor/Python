num = int(input('Enter temparature: '))

print('1. Celcius to Farenheit\n2. Farenheit to Celcius')
choice = int(input('Enter choice: '))
if (choice == 1):
    Farenheit = (Celcius * 1.8) + 32
    print('%0.1f degree Celcius is equal to %0.1f degree Ferenheit.' %(num, Farenheit))

else:
    Celcius = (num - 32) / 1.8
    print('%0.1f degree Farenheit is equal to %0.1f degree Celcius.' %(num, Celcius))
