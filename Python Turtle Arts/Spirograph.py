# Original - https://www.youtube.com/watch?v=Jmg99sKAxqQ&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=9

from turtle import *

speed(0)
bgcolor("cyan")
pensize(2)

for i in range(6):
    for colours in ["blue", "magenta", "yellow", "hotpink", "pink", "skyblue", "orange"]:
        color(colours)
        circle(100)
        left(10)

hideturtle()

done()

