from turtle import *

speed(0)
setup(800, 600)
pensize(10)

pencolor("black")
circle(80)

penup()
goto(-200, 0)
pendown()
pencolor("blue")
circle(80)

penup()
goto(200, 0)
pendown()
pencolor("red")
circle(80)

penup()
goto(-100, -100)
pendown()
pencolor("yellow")
circle(80)

penup()
goto(100, -100)
pendown()
pencolor("green")
circle(80)

hideturtle()

done()

