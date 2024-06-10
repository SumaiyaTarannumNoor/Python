# Original - https://www.youtube.com/watch?v=XPppF-rgQGE&list=PLVe8Xn841DPOzALiuGXKM1FU-8hqs2sMo&index=12

from turtle import *

setup(800, 600)
bgcolor("black")
pensize(10)
speed(0)

colours = ["blue", "magenta", "yellow", "hotpink", "pink", "skyblue", "orange", "red", "green", "cyan"]

for i in range(300):
    color(colours[i % 10])
    forward(i * .6)
    left(100)
    forward(i * .6)
    right(160)

hideturtle()

done()
