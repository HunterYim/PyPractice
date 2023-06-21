import turtle
import random
import math
import time

# 기본 윈도우 세팅
wn = turtle.Screen()
wn.title("JUMP GAME")
wn.bgcolor("skyblue")
wn.setup(height=600, width=1200)
wn.tracer(0)

# 바닥 생성
gl = turtle.Turtle()
gl.color("green")
gl.speed(0)
gl.shape("square")
gl.penup()
gl.goto(0, -280)
gl.shapesize(stretch_len=1000, stretch_wid=2)

gravity = -0.005    # 중력
count = 0           # 체리 충돌 카운팅
score = 0           # 점수

# 점수 출력을 위한 펜 세팅
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()
pen.goto(-580, 260)
pen.pendown()
pen.color("red")
pen.write(f"{score} 점", False, "left", ("", 20)) # 점수 출력

# 이미지 가져오기
shapes = ["goblin.gif", "pacman.gif", "cherry.gif"]
for shape in shapes:
    wn.register_shape(shape)


# 스프라이트 클래스 선언
class Sprite(turtle.Turtle):
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = width
        self.height = height
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.shape(self.image)
        self.penup()
        self.goto(x, y)
        self.state = "ready"
        self.dx = 0
        self.dy = 0

    # 충돌 감지 방법: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    # aabb: Axis Aligned Bounding Box
    def is_aabb_collision(self, other):
        x_collision = abs(self.xcor() - other.xcor()) * 2 < (self.width + other.width)
        y_collision = abs(self.ycor() - other.ycor()) * 2 < (self.height + other.height)
        # x_collision = (math.fabs(self.xcor() - other.xcor()) * 2) < (self.width + other.width)
        # y_collision = (math.fabs(self.ycor() - other.ycor()) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

# 객체 생성 및 이동
pacman = Sprite(-350, -197, 70, 70, "pacman.gif")
goblin = Sprite(555, -210, 60, 60, "goblin.gif")
cherry = Sprite(545, 0, 100, 100, "cherry.gif")
goblin.dx = random.randint(4, 6) * -0.1
cherry.dx = random.randint(2, 5) * -0.1

# 팩맨 동작 함수
def jump():
    if pacman.state == "ready": 
        pacman.dy = 1.5
        pacman.state = "jumping"

def right():
    if pacman.state == "ready":
        pacman.dx = 0.3
        
def left():
    if pacman.state == "ready":
        pacman.dx = -0.3

def stop():
    if pacman.state == "ready":
        pacman.dx = 0

# 이벤트 처리
wn.listen()
wn.onkeypress(jump, "space")
wn.onkeypress(right, "Right")
wn.onkeypress(left, "Left")
wn.onkeypress(stop, "Down")

# 메인 루프
while True:
    wn.update() # 화면 업데이트

    pacman.dy += gravity # 팩맨 중력 작용

    # 팩맨 점프
    y = pacman.ycor()
    y += pacman.dy
    pacman.sety(y)
    pacman.state = "jumping"

    # 팩맨 좌우 이동
    x = pacman.xcor()
    x += pacman.dx
    pacman.setx(x)
    pacman.state = "jumping"
    
    # 고블린 이동
    x = goblin.xcor()
    x += goblin.dx
    goblin.setx(x)

    # 체리 이동
    x = cherry.xcor()
    x += cherry.dx
    cherry.setx(x)

    # 고블린 재생성
    if goblin.xcor() < -700:
        goblin = Sprite(555, -210, 128, 128, "goblin.gif")
        goblin.dx = random.randint(4, 6) * -0.1

    # 체리 재생성
    if cherry.xcor() < -700:
        cherry = Sprite(545, 0, 128, 128, "cherry.gif")
        cherry.dx = random.randint(2, 5) * -0.1

    # 팩맨 바닥 위로 고정
    if pacman.ycor() < -197:
        pacman.sety(-197)
        pacman.state = "ready"

    # 팩맨 좌측 벽 충돌
    if pacman.xcor() < -533:
        pacman.setx(-533)
    
    # 팩맨 우측 벽 충돌
    if pacman.xcor() > 527:
        pacman.setx(527)


    # 팩맨-고블린 충돌 여부 확인
    if pacman.is_aabb_collision(goblin):
        time.sleep(2)
        break
    
    # 팩맨-체리 충돌 여부 확인
    if pacman.is_aabb_collision(cherry):
        cherry.hideturtle()
        count += 2
        score = count // 5
        # 점수 출력
        if score % 20 == 0:
            pen.clear()
            pen.write(f"{score} 점", False, "left", ("", 20))