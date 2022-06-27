import random

def computer_guess(x):
    low = 1000
    high = x
    feedback = ''
    
    while feedback != 'c':
        if low!=high:
            guess = random.randint(low, high)
        else: 
            guess = low #could be high as well
        feedback= input(f'Is {guess} too high (H), too low(L), correct(C)?: \n').lower()
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1    
                  
    print(f'The computer has guessed the number correctly!!!!')

computer_guess(2050)                          