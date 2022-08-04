from src.Utilites import *
from math import floor


class Game:
    ball=None
    paddle_speed=8
    ball_speed=4
    board_to_paddle_distance=50
    board_width=0
    board_height=0
    Max_Points=3 #to win
    final_result=3 #3: not known, 2:draw,0:left vicotry, 1:right victory
    Max_Touches=200#leads to draw if no one has higher points!
    num_touches=0
    total_touches=[0,0]
    players=[]
    step_number=0
    num_games=0
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
        self.num_touches=0
        
    def nextGameStep(self):
        rewards=[0,0]
        score_reward=2
        win_reward=3
        touch_reward=10
        draw_reward=11
        if self.final_result==3:
            #print("into game step")
            self.step_number+=1
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
                self.num_touches+=1
                self.total_touches[side]+=1
                rewards[side]+=touch_reward
                self.ball.reverseLeftRight((-1)**(side)*1.5*del_y/self.players[side].paddle.height/2,side)
            self.ball.moveOneStep()

            if self.num_touches==self.Max_Touches:
                self.players[1].points+=1
                self.players[0].points+=1
                rewards[0]+=draw_reward
                rewards[1]+=draw_reward
                self.resetBoard(random.randint(0, 1))
            elif (self.ball.position[0]-self.ball.diameter/2)<=-self.board_width/2:
                #right scored!
                rewards[1]+=score_reward
                rewards[0]-=score_reward
                self.players[1].points+=1
                self.resetBoard(0)
            elif (self.ball.position[0]+self.ball.diameter/2)>=self.board_width/2:
                self.players[0].points+=1
                self.resetBoard(1)
                rewards[1]-=score_reward
                rewards[0]+=score_reward
            
            if self.players[0].points==self.Max_Points and self.players[0].points>self.players[1].points:
                self.final_result=0 #left wins
                rewards[1]-=win_reward
                rewards[0]+=win_reward
                self.num_games+=1
            elif self.players[1].points==self.Max_Points and self.players[0].points<self.players[1].points:
                self.final_result=1 #right wins
                rewards[1]+=win_reward
                rewards[0]-=win_reward
                self.num_games+=1
            elif self.players[1].points==self.Max_Points and self.players[0].points==self.players[1].points:
                self.final_result=2 #draw
                self.num_games+=1
        else:
            print("The Result of the game is known and no further action is possible! You could restart the game.")
        return rewards

    def restartSameGame(self):
        r1=random.randint(0, 1)
        r2=random.random()
        theta=r1*pi-pi/4+r2*pi/2

        self.ball.resetPosition()
        self.ball.step=[self.ball_speed*cos(theta),self.ball_speed*sin(theta)]

        for p in self.players:
            p.paddle.resetPosition()
            p.points=0
        
        self.num_touches=0
        self.total_touches=[0,0]
        self.step_number=0
        self.final_result=3

    def getState(self,side):
        weight=10
        player_y=self.players[side].paddle.position[1]/weight
        ball_y=self.ball.position[1]/weight
        delx=abs(self.ball.position[0]-self.players[side].paddle.position[0])/weight
        dely=abs(self.players[side].paddle.position[1]-self.ball.position[1])
        points1=self.players[side].points
        points2=self.players[1-side].points
        ball_vy=self.ball.step[1]
        ntouches=self.total_touches[side]

        return (player_y,ball_y,dely,delx,ntouches,self.final_result)
'''
        x5=self.ball.position[0]
                x7=self.ball.step[0]
    def getState(self,side):
        # 0,1: self.position, 2: self.points, 3,4: enemy.position, 5: enemy.points, 6: paddle.speed, 
        # 7,8: ball.position, 9,10: ball.speed, 11: num_touches 12: final_result
        x0=self.players[side].paddle.position[0]
        x1=self.players[side].paddle.position[1]
        x2=self.players[side].points
        x3=self.players[1-side].paddle.position[0]
        x4=self.players[1-side].paddle.position[1]
        x5=self.players[1-side].points
        x6=self.players[0].paddle.step
        x7=self.ball.position[0]
        x8=self.ball.position[1]
        x9=self.ball.step[0]
        x10=self.ball.step[1]
        x11=self.num_touches
        x12=self.final_result

        return (x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12)'''