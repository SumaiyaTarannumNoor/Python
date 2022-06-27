import random

def guess(x):
    random_number = random.randint(1, x)
    guess = 0
    while guess != random_number:
        guess= int(input(f'Guess a number between 1 and {x}: \n'))
        if guess > random_number:
            print("Sorry! too high.")
        elif guess < random_number:
            print("Sorry! too low.")    
            
    print(f'Wooho!! You have correctly guessed the number {random_number}!!! Congratulations.')

guess(16)            