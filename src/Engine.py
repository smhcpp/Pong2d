from src.Utilites import *
import random
import math
import numpy as np
import torch
from collections import deque
from src.Model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000


def getDistance(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class RandEngine(Agent):
    def __init__(self,name, side, paddle):
        super(RandEngine,self).__init__(name, side, paddle, True)
    
    def getAction(self,state):
        return random.randint(0, 2)


class BFEngine(Agent):
    def __init__(self,name, side, paddle):
        super(BFEngine,self).__init__(name, side, paddle, True)
    """
    def getAction(self,state):
        pos=[state[0],state[1]]
        bpos=[state[7],state[8]]
        pspeed=self.paddle.step
        p0=[pos[0],pos[1]+pspeed]
        p1=[pos[0],pos[1]-pspeed]
        d=np.array([getDistance(p0, bpos),getDistance(p1, bpos),getDistance(pos, bpos)])
        return np.argmin(d)"""
    def getAction(self,state):
        weight=10
        pos=state[0]*weight
        bpos=state[1]*weight
        pspeed=self.paddle.step
        d=np.array([abs(pos+pspeed-bpos),abs(pos-pspeed-bpos),abs(pos-bpos)])
        return np.argmin(d)

class RiEngine(Agent):
    def __init__(self,name, side, paddle,is_model_loaded):
        super(RiEngine,self).__init__(name, side, paddle, True)
        self.num_games = 0
        self.least_game_number=10
        self.epsilon = 0.005 # randomness
        self.lr=0.0001
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.is_model_loaded=is_model_loaded
        self.model = Linear_QNet(4, 32,16, 3)
        if self.is_model_loaded:
            path="model/model_touch-115.pth"
            self.model.load_state_dict(torch.load(path))
            self.num_games=self.least_game_number+1
            self.model.eval()
        
        self.trainer = QTrainer(self.model, lr=self.lr, gamma=self.gamma)
    
    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state)) # popleft if MAX_MEMORY is reached
    
    def trainMemory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states = zip(*mini_sample)
        self.trainer.trainStep(states, actions, rewards, next_states)

        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def getAction(self,state):
        move =2
        if random.random() < self.epsilon or self.num_games<self.least_game_number:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        return move
