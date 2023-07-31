import random

COLORS = ['P', 'B', 'R', 'Y', 'O', 'W']
Tries = 7
CODE_LENGTH = 4

def generate():
    code = []

    for _ in range(CODE_LENGTH):
        color = random.choice(COLORS)
        code.append(color)
    return code

code = generate()

def guess_code():
    while True:
        guess = input("Guess the colors: ").upper().split(" ")

        if len(guess) != CODE_LENGTH:
            print(f"You must make {CODE_LENGTH} guess.")
            break

        for color in guess:
            if color not in COLORS:
                print(f"Invalid Guess: {color}. Try Again.")
                break

        else:
            break

    return guess

def check(guess, real):
    color_count = {}
    correct_pos = 0
    incorrect_pos = 0

    for color in real:
        if color not in color_count:
            color_count[color] = 0
        color_count[color] += 1

    for guess, real in zip(guess, real):
        if guess == real:
            correct_pos += 1
            color_count[guess] -= 1

    for guess, real in zip(guess, real):
        if guess in real and color_count[guess] > 0:
            incorrect_pos += 1
            color_count[guess] -= 1

    return correct_pos, incorrect_pos

def game():
    print(f"Welcome to Matermind Game. You have {Tries} tries to guess the colors. Enjoy!!!")
    print("Valid colors are:", *COLORS)
    code = generate()
    for attempts in range(1, Tries+1):
        guess = guess_code()
        correct_pos, incorrect_pos = check(guess, code)

        if correct_pos == CODE_LENGTH:
            print(f"Congratulations! You have guessed the code in {attempts} tries.")
            break

        print(f"Correct Positions:{correct_pos} | Incorrect Positions: {incorrect_pos}")

    else:
        print("You ran out of tries. The code was: ", *code)

if __name__ == "__main__":
    game()







