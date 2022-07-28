from src.Utilites import *
from math import floor

class Game:
    ball=None
    paddle_speed=8
    ball_speed=paddle_speed/4
    board_to_paddle_distance=50
    board_width=0
    board_height=0
    players=[]
    turn=0 #0:left, 1:right
    
    def __init__(self,boardwidth,boardheight,left_player_name,right_player_name,left_player_isBot,right_player_isBot):
        self.board_width=boardwidth
        self.board_height=boardheight
        r1=random.randint(0, 1)
        r2=random.random()
        theta=r1*pi-pi/4+r2*pi/2
        self.ball=Ball([0,0], [self.ball_speed*cos(theta),self.ball_speed*sin(theta)])

        posx=self.board_width/2-self.board_to_paddle_distance
        paddle=Paddle([-posx,0], self.paddle_speed)
        self.players.append(Agent(left_player_name, 0,paddle,left_player_isBot))
        paddle2=Paddle([posx,0], self.paddle_speed)
        self.players.append(Agent(right_player_name, 1,paddle2,right_player_isBot))

    def resetBoard(self,side):
        for p in self.players:
            p.paddle.resetPosition()
        self.ball.resetPosition()
        speed=[0,0]
        speed[0]=(-1)**(side+1)*self.ball_speed
        self.ball.step=speed
        
    def gameLoop(self):
        cond1=self.ball.position[1]+self.ball.step[1]+self.ball.diameter/2>self.board_height/2
        cond2=self.ball.position[1]+self.ball.step[1]-self.ball.diameter/2<-self.board_height/2
        if cond1 or cond2:
            self.ball.reverseUpDown()
        
        side=0 # to the left side
        if self.ball.step[0]>0:
            side=1 # to the right side
        cond3=abs(self.ball.position[0]+self.ball.step[0]-self.players[side].paddle.position[0])<=self.ball.diameter/2+(-1)**(side+1)*self.players[side].paddle.thickness/2
        del_y=self.ball.position[1]-self.players[side].paddle.position[1]
        cond4=abs(self.ball.position[1]+self.ball.step[1]-self.players[side].paddle.position[1])<=self.ball.diameter/2+self.players[side].paddle.height/2
        if cond3 and cond4:
            self.ball.reverseLeftRight((-1)**(side)*1.5*del_y/self.players[side].paddle.height/2,side)
        self.ball.moveOneStep()

        if (self.ball.position[0]-self.ball.diameter/2)<=-self.board_width/2:
            #right scored!
            self.players[1].points+=1
            self.resetBoard(0)
        elif (self.ball.position[0]+self.ball.diameter/2)>=self.board_width/2:
            self.players[0].points+=1
            self.resetBoard(1)