# Original - https://www.youtube.com/watch?v=iV1m06K3xWY&list=PLVe8Xn841DPOzALiuGXKM1FU-8hqs2sMo&index=11

from turtle import *

setup(600, 500)
bgcolor("black")
pensize(20)
speed(4)

colours = ["blue", "magenta", "yellow", "hotpink", "pink", "skyblue", "orange", "red", "green", "cyan"]

for i in range(80):
    pencolor(colours[ i % 6])
    width( i / 5 + 1 )
    forward(i)
    left(20)

hideturtle()

done()