# Original - https://www.youtube.com/watch?v=8RdhPPKq5AI&list=PLS9qLR8VoFA56NWSswK2daQSovI9QCpQE&index=41

from turtle import *

speed(6)
bgcolor("royalblue")

penup()
goto(-100, 0)
pendown()

color("hotpink", "cyan")
begin_fill()
for i in range(4):
    forward(200)
    right(90)

left(90)
for i in range(3):
    forward(200)
    right(90)

end_fill()

penup()
goto(0, 140)
pendown()
color("hotpink")
begin_fill()
circle(30)
end_fill()

penup()
goto(-40, -20)
pendown()
begin_fill()
circle(30)
end_fill()

penup()
goto(40, -120)
pendown()
begin_fill()
circle(30)
end_fill()

hideturtle()


done()
