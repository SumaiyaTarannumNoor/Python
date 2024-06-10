# Original - https://www.youtube.com/watch?v=_JxgaQ4xT3E&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=11

from turtle import *

speed(0)
bgcolor("black")

colours = ["blue", "magenta", "yellow", "hotpink", "pink", "skyblue", "orange", "red", "green", "cyan"]

for i in range(360):
    pencolor((colours[i%6]))
    width( i / 250 + 1 )
    forward(i)
    left(59)

hideturtle()

done()