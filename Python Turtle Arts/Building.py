# Original - https://www.youtube.com/watch?v=exsn0aVTTlo&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=43

from turtle import *

speed(0)
bgcolor("deepskyblue")

#dome
penup()
goto(0, 20)
pendown()
color("deeppink")
begin_fill()
circle(100)
end_fill()


#first bottom layer
penup()
goto(-200, -200)
pendown()
color("medium violet red")
begin_fill()
for i in range(2):
    forward(400)
    left(90)
    forward(20)
    left(90)
end_fill()

#seond bottom layer
penup()
goto(-175, -180)
pendown()
color("hotpink")
begin_fill()
for i in range(2):
    forward(350)
    left(90)
    forward(20)
    left(90)
end_fill()

# Main Building
penup()
goto(-150, -160)
pendown()
begin_fill()
color("violet")
for i in range(2):
    forward(300)
    left(90)
    forward(250)
    left(90)
end_fill()

#second top rectangle
penup()
goto(-175, 90)
pendown()
color("hotpink")
begin_fill()
for i in range(2):
    forward(350)
    left(90)
    forward(20)
    left(90)
end_fill()

# Top rectangle
penup()
goto(-150, 110)
pendown()
begin_fill()
color("medium violet red")
for i in range(2):
    forward(300)
    left(90)
    forward(20)
    left(90)
end_fill()



hideturtle()

done()

