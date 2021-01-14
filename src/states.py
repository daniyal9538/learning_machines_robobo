import numpy as np
from random import randint, uniform
from actions import *

class Agent:
    def __init__(self,rob, **args):
        self.rob = rob
        self.state_variables = ['robot_position', 'sensor_state','stuck_state', 'sensor_data' ]
        self.previous_states = []
        self.previous_data = {}
        self.current_state =[]
        self.current_data = {}
        self.stuck_threshold = args.get('stuck_threshold',0.05)
        self.debug_print = args.get('debug_print', False)
        self.current_reward = 0
        self.reward_history = []
        self.q_table = args.get('q_table',np.zeros(shape=(2,2,2,2,2,2,6)))
        self.alpha = args.get('alpha',0.3)
        self.gamma = args.get('gamme', 0.9)
        self.n_episodes = args.get('n_episodes', 10)
        self.epsilon = args.get('epsilon', 0.4)
        self.max_steps = args.get('max_steps', 50)
        self.current_action = None
        self.action_history = []

        for i in self.state_variables:
            self.previous_data[i] = []

    def createSensorState(self, sensor_input):
        sensor_input = [1 if i>0 else 0 for i in sensor_input]
        return sensor_input

    def generateMoveFromPolicy(self):
        if self.generateEpsilon():
            selected_move = self.generateRandomMove()
        else:
            selected_move = self.generateGreedyMove()
            
        return selected_move

    def generateEpsilon(self):
        if uniform(0,1) <= self.epsilon:
            return True
        return False
    
    def generateRandomMove(self):
        return randint(0,5)

    def generateGreedyMove(self):
        # state = np.array(self.current_state)
        candidate_values = self.q_table[tuple(self.current_state)]
        return np.random.choice(np.flatnonzero(candidate_values == candidate_values.max()))

    def calculateQValue(self, max_q, old_q, reward):
        return ((1-self.alpha)*(old_q) + self.alpha*(reward + self.gamma*(max_q)-old_q))

    def updateState(self, **state):
        self.current_action = state.get('action',None)
        self.action_history.append(self.current_action)
        state['sensor_state'] = self.createSensorState(state.get('sensor_data',None))
        for i in self.state_variables:
            if i == 'stuck_state':
                _state = self.isStuck()
            else: 
                _state = state.get(i, None)
            self.current_data[i] = _state
            self.previous_data[i].append(_state)
            # print(self.current_data)
        self.current_state = [self.current_data['stuck_state']] + self.current_data['sensor_state']
        self.previous_states.append(self.current_data)
        self.generateRewards()
        # self.updateQTable()

    def isStuck(self):
        if len(self.previous_data['robot_position']) <= 1:
            # print(000)
            # return False
            return 0
        # print(1,self.previous_states['robot_position'])
        curr = self.previous_data['robot_position'][-1]
        prev  = self.previous_data['robot_position'][-2]
        arr = np.absolute(np.subtract(curr ,prev))
        # print(arr)
        # print(2)
        if self.debug_print:
            print(arr)
        return (int(all(i <= self.stuck_threshold for i in arr)))

    def generateRewards(self):
        # reward for staying stuck -2
        # reward for having detected something in sensor -1
        reward = self.current_data['stuck_state']*-2
        reward += sum(self.current_data['sensor_state'])*-1
        self.current_reward = reward
        self.reward_history.append(reward)

    # def updateQTable(self, old_q, max_q, reward):
        


    def runEpisode(self):
        
        next_move = self.generateMoveFromPolicy()
        self.executeMove(next_move)
    
    def executeMove(self, move):
        old_state = self.current_state
        selectMove(self.rob, action = move)
        sensor_data = self.rob.read_irs()[3:]
        current_data = {'robot_position':self.rob.position(),
                            # 'sensor_state':sensor_input,
                            'sensor_data':sensor_data,
                            'action':move
                            }
        self.updateState(**current_data)
        new_state = self.current_state
        reward = self.current_reward
        old_q = self.q_table[tuple(old_state)][move]
        max_q = np.max(self.q_table[tuple(new_state)])
        self.q_table[tuple(old_state)][move] = self.calculateQValue(max_q=max_q, old_q=old_q, reward=reward)


    def initEnv(self):
        self.previous_states = []
        self.previous_data = {}
        self.current_state =[]
        self.current_data = {}
        self.current_action = None
        self.action_history = []
        self.current_reward = 0
        self.reward_history = []
        for i in self.state_variables:
            self.previous_data[i] = []
        self.rob.stop_world()
        self.rob.play_simulation()


    def train(self):
        for _ in range(self.n_episodes):
            self.initEnv()
            first_move = self.generateRandomMove()
            self.executeMove(first_move)
            print(f'Episode {_}: ', end = '')
            for i in range(self.max_steps):

                next_move = self.generateMoveFromPolicy()
                self.executeMove(next_move)
            print(f'End state: {self.current_state}')
            print(f'End reward: {self.current_reward}')
            print(f'Total reward accumulated {sum(self.reward_history)}')
        self.rob.stop_world()
        print('Training Finished')



