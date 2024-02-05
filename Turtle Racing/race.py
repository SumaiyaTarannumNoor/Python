import turtle
import time
import random

WIDTH, HEIGHT = 600, 600
COLORS = ['blue', 'pink', 'cyan', 'blueviolet', 'violet', 'brown', 'magenta', 'green', 'lavender', 'blueviolet', 'navy', 'red', 'gold', 'royalblue', 'yellow', 'orange']

def get_number_of_racers():
    racers = 0
    while True:
        racers = input("Enter the number of racers (2-16): ")

        if racers.isdigit():
            racers = int(racers)
        else:
            print("Input is not valid. Try again.")
            continue

        if 2 <= racers <= 16:
            return racers
        else:
            print("Number is not in the range of (2-16). Try again")


def race(colors):
    turtles = create_racers(colors)

    while True:
        for racer in turtles:
            distance = random.randrange(1, 20)
            racer.forward(distance)

            x,y = racer.pos()
            if y>= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)]
def create_racers(colors):
    turtles = []
    spacingX = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDTH//2 + (i + 1) * spacingX, -HEIGHT//2 + 20)
        racer.pendown()
        turtles.append(racer)
    return turtles
def init_turtle():
    SCREEN = turtle.Screen()
    SCREEN.setup(WIDTH, HEIGHT)
    SCREEN.title('Naruto Racing!!!')


racers = get_number_of_racers()
init_turtle()

random.shuffle(COLORS)
colors = COLORS[:racers]

winner = race(colors)
print(winner)
