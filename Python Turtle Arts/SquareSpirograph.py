# Original - https://www.youtube.com/watch?v=Vp2E-kH87Is&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=10

from turtle import *

speed(0)
bgcolor("black")
pensize(2)

for i in range(6):
    for colours in ["blue", "magenta", "yellow", "hotpink", "pink", "skyblue", "orange", "red", "green", "cyan"]:
        color(colours)
        left(12)
        for i in range(4):
            forward(200)
            left(90)

hideturtle()

done()

