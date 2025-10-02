# import turtle

# turtle.title('거북이 그래픽스')
# turtle.setup(500,500)
# turtle.bgcolor('black')

# t = turtle.Turtle()
# t.shape('turtle')
# t.color('white','orange')
# t.pencolor('skyblue')
# t.pensize(1)

# t.right(360/10)
# length = 3
# for j in range(10):
#     for i in range(5):
#         t.right(360/5)
#         t.forward(length)
#         length += 2

# turtle.exitonclick()


import turtle

turtle.title('거북이 그래픽스')
turtle.setup(500,500)
turtle.bgcolor('skyblue')
turtle.update()

star = turtle.Turtle()
star.shape('turtle')
star.color('yellow')
star.speed(0)


# colors = ['red', 'yellow', 'blue', 'green', 'purple']

def drawStar(x, y):
    star.penup()
    star.goto(x,y)
    star.setheading(0)
    star.color('yellow')
    star.fillcolor('yellow')
    star.pendown()
    star.begin_fill()
    for i in range(5):
        star.forward(20)
        star.left(72)
        star.forward(20)
        star.right(144)
    star.end_fill()
    star.hideturtle()

drawStar(-70,150)
drawStar(-150,200)
drawStar(180,200)
drawStar(100,-00)

rainbow = turtle.Turtle()
rainbow.shape('turtle')
rainbow.color('white','black')
rainbow.pensize(5)
rainbow.speed(0)

rainbows_colors = ['red', 'orange', 'yellow', 'green', 
                   'blue', 'navy','purple']

def drawRainbow(radius, x , y):
    rainbow.penup()
    rainbow.goto(x,y)
    rainbow.setheading(0)
    rainbow.forward(radius)
    for i in range(len(rainbows_colors)):
        rainbow.pendown()
        rainbow.left(90)
        rainbow.color(rainbows_colors[i])
        rainbow.circle(radius, 180)
        rainbow.penup()
        rainbow.left(90)
        radius -= 5
        rainbow.forward(5+2*radius)
    rainbow.penup()
    k = 20
    for i in range(3):
        rainbow.goto(x+radius+k,y)
        rainbow.setheading(90)
        rainbow.pendown()
        rainbow.color('white','white')
        rainbow.begin_fill()
        rainbow.circle(15)
        rainbow.end_fill()
        rainbow.penup()
        k += 15
    k = 20
    for i in range(3):
        rainbow.goto(x-radius-k,y)
        rainbow.setheading(90)
        rainbow.pendown()
        rainbow.color('white','white')
        rainbow.begin_fill()
        rainbow.circle(15)
        rainbow.end_fill()
        rainbow.penup()
        k -= 15
    rainbow.hideturtle()

drawRainbow(100, -70, -120)
drawRainbow(70, 100, 100)
drawRainbow(50, -100, 70)
turtle.exitonclick()