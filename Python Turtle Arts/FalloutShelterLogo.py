# Original - https://www.youtube.com/watch?v=DMx9Ce6K5Ro&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=42

from turtle import *

speed(0)
bgcolor("gold")

penup()
goto(0, -230)
pendown()
color("black")
begin_fill()
circle(225)
end_fill()


penup()
goto(0, 0)
pendown()
color("gold")
begin_fill()

for i in range(3):
    right(120)
    for i in range(3):
        forward(200)
        right(120)
end_fill()


hideturtle()

done()

