#Modules
import turtle as tr
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from scoreboard import Scoreboard
from ui import UI
import time

#Create window
screen = tr.Screen()
screen.bgcolor("black")
screen.setup(width=1200, height=600)
screen.title("Breakout")
screen.tracer(0)

ui = UI()
ui.header()
score=Scoreboard(lives=5)
paddle = Paddle()
ball = Ball()
bricks = Bricks()

#Variables
game_paused = False
playing_game = True

#Functions
#Pause Game function
def pause_game():
    global game_paused
    if game_paused:
        game_paused = False
    else:
        game_paused = True

#Check to see whether the ball collides with the wall
def check_collision_with_walls():
    global ball, score, playing_game, ui
    if ball.xcor() < -500 or ball.xcor() > 570:
        ball.bounce(x_bounce=True, y_bounce=False)
        return
    if ball.ycor() > 270:
        ball.bounce(x_bounce=False, y_bounce = True)
        return
    if ball.ycor() < -280:
        ball.reset()
        score.decrease_lives()
        if score.lives == 0:
            score.reset()
            playing_game = False
            ui.game_over(win=False)
            return
        ui.change_color()
        return

#Check to see whether the ball collides with the paddle
def check_collision_with_paddle():
    global ball, paddle 
    paddle_x = paddle.xcor()
    ball_x = ball.xcor()
    if ball.distance(paddle) < 110 and ball.ycor() < -250:
        if paddle_x > 0:
            if ball_x > paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return
        elif paddle_x < 0:
            if ball_x < paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce= True)
                return
        else:
            if ball_x > paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            elif ball_x < paddle_x:
                    ball.bounce(x_bounce=True, y_bounce=True)
                    return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)

#Check to see whether the ball collides with the bricks
def check_collision_with_bricks():
    global ball, bricks
    for brick in bricks.bricks:
        if ball.distance(brick) < 40:
            brick.quantity -= 1
            if brick.quantity == 0:
                brick.clear()
                brick.goto(3000, 3000)
                bricks.bricks.remove(brick)
            if ball.xcor() < brick.left_wall:
                ball.bounce(x_bounce=True, y_bounce=False)
            elif ball.xcor() > brick.right_wall:
                ball.bounce(x_bounce=True, y_bounce=False)
            elif ball.ycor() < brick.bottom_wall:
                ball.bounce(x_bounce=False, y_bounce=True)
            elif ball.ycor() > brick.upper_wall:
                ball.bounce(x_bounce=False, y_bounce=True)      

#Paddle Movement
screen.listen()
screen.onkey(paddle.move_left, "Left")
screen.onkey(paddle.move_right, "Right")
screen.onkey(pause_game, "space")


while playing_game:
    if game_paused:
        screen.update()
        time.sleep(0.01)
        ball.move()
        check_collision_with_walls()
        check_collision_with_bricks()
        check_collision_with_paddle()
        if len(bricks.bricks) == 0:
            ui.game_over(win=True)
            break
    else:
        ui.paused_status()

tr.mainloop()