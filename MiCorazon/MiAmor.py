import turtle as t
WIDTH, HEIGHT = 600, 600
pen = t.Turtle()
t.bgcolor('#ffffff')
t.delay(6)
pen.color('#0643cf')
pen.begin_fill()
pen.left(42)
pen.forward(121.01)
pen.circle(80, 190)
pen.right(100.02)
pen.circle(80, 181.08)
pen.forward(160)
pen.left(90)
pen.forward(50)
pen.setpos(-60, 100)
pen.end_fill()
def txt():
    # pen.up()
    pen.setpos(-80, 80)
    pen.color('#175cff')
    pen.write('😊', font=("Segoe UI Emoji", 60))
    pen.up()
    pen.setpos(-62, 40)
    pen.color('#175cff')
    pen.write('Mi Amor', font=("Segoe UI Emoji", 16))
    pen.color('#0643cf')
txt()
pen.end_fill()
t.exitonclick()