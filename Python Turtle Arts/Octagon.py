# Original - https://www.youtube.com/watch?v=WiShwgtWWHI&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=8

from turtle import *


setup(800, 600)
speed(6)
bgcolor("black")
color("cyan")
pensize(6)

for i in range(8):
    left(45)
    for i in range(8):
        forward(100)
        left(45)

done()
