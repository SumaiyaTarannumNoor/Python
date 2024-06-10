# Original - https://www.youtube.com/watch?v=q28BxST9b94&list=PLVe8Xn841DPOzALiuGXKM1FU-8hqs2sMo&index=9
import colorsys
from turtle import *

speed(0)
bgcolor("skyblue")
num_of_colours = 7
colours = ["violet", "blue", "green", "yellow", "orange", "red"]

def draw_arch(x, y, r, pen_size, color):
    penup()
    goto(x + r, y)
    pendown()
    seth(90)
    pensize(pen_size)
    pencolor(color)
    circle(r, 180)

radius = 160
penwidth = 20 * 7 / num_of_colours
hue = 0
for i in range(num_of_colours):
    (red, green, blue) = colorsys.hsv_to_rgb(hue, 1, 1)
    draw_arch(0, -100, radius, penwidth, (red, green, blue))
    radius -= (penwidth - 1)
    hue += 0.9 / num_of_colours

hideturtle()

done()
