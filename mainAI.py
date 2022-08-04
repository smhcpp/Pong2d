import threading
import time
from src.Engine import *
from src.Game import *


def print_state(state):
    print(f'points: {state[-4]} - {state[-3]}, final_result: {state[-1]}')

def startGame():
    game=Game(600, 300, "Mortimer", "Blake",True, True)

    engine0=BFEngine(game.players[0].name, game.players[0].side, game.players[0].paddle)
    engine1=RiEngine(game.players[1].name, game.players[1].side, game.players[1].paddle,False)
    results=np.array([0,0,0])
    score_sum=np.array([0,0])
    reward_record=-200.
    touch_record=0
    Max_Num_Games=1_000
    for i in range(Max_Num_Games):
        total_reward=np.array([0.,0.])
        while game.final_result==3:
            #get old states
            state0=game.getState(0)
            state1=game.getState(1)

            #get new actions
            action0=engine0.getAction(state0) # up:0, down:1, nothing:2
            state1p=(state1[2],state1[3],state1[4],state1[5])
            action1=engine1.getAction(state1p) # up:0, down:1, nothing:2

            #get the rewards for actions
            game.players[0].movePaddle(action0,game.board_height)
            game.players[1].movePaddle(action1,game.board_height)
            rewards=game.nextGameStep()
            total_reward[1]+=rewards[1] 
            total_reward[0]+=rewards[0]

            #get new states
            #new_state0=game.getState(0) We are training only the right one now
            new_state1=game.getState(1)
            new_state1p=(new_state1[2],new_state1[3],new_state1[4],new_state1[5])

            #engine1.trainShortMemory(state1p, action1, rewards[1], new_state1p) 
            #if new_state1[-1]!=3:
            #    print(new_state1)
            #done=final_result of new_state1
            
            #remember this move:
            engine1.remember(state1p, action1, rewards[1], new_state1p) 

        engine1.trainMemory()
        if total_reward[1]>reward_record:
            #print("higher reward",total_reward)
            reward_record=total_reward[1]
            #touch_record=game.total_touches[1]
            engine1.model.save()
        if touch_record<game.total_touches[1]:
            touch_record=game.total_touches[1]
        #    engine1.model.save()  

        engine1.num_games+=1

        results[game.final_result]+=1

        score_sum[0]+=game.players[0].points
        score_sum[1]+=game.players[1].points
        
        print('Game', engine1.num_games, ',Reward Record:', reward_record, ',Touch Record:',touch_record,',Total Touches:',game.total_touches[1])
        print(f'Score: {game.players[0].points} - {game.players[1].points}, Total Scores: {score_sum[0]} - {score_sum[1]}')
        if game.final_result==2:
            print("Game was drawn!")
        else:
            print(game.players[game.final_result].name+" is Victorious!!!!")
        #print_state(game.getState(0))
        print("____________________________________")
        game.restartSameGame()
        
    #return game.final_result
    print(results/Max_Num_Games)
    print(score_sum/(score_sum.sum()))


startGame()
