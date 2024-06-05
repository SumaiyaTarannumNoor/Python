from turtle import *
from random import randint

# Page setup
setup(800, 600)
speed(0)
bgcolor("black")

# Function to draw one star
def star():
    color("yellow")
    begin_fill()
    for i in range(6):
        forward(16)
        right(144)
    end_fill()


# Function to draw multiple stars at random location
for i in range (40):
    penup()
    goto(randint(-400, 400), randint(-300, 300))
    pendown()
    star()

# Moon - Part 1
penup()
goto(-300, 100)
pendown()
color("white")
begin_fill()
circle(60)
end_fill()

# Moon - Part 2
penup()
goto(-280, 100)
pendown()
color("black")
begin_fill()
circle(60)
end_fill()

# Keep the screen open
done()
