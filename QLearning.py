import numpy as np
import random

# TODO

class QLearning:
    def __init__(self):
        self.qtable = None
        self.alfa = 0.5
        self.gamma = 0.9
        self.epsilon = 0.5

    # Set the qtable with a previous calculated one
    def set_model(self, model):
        self.qtable = model

    # Return the action to play
    def act(self, state):
        state_ID = state.get_state_ID()

        action = np.argmax(self.qtable[state_ID-1, :])
        return action + 1

    # Learn the qtable
    def learn(self, state, max_iters):
        self.qtable = np.zeros((state.get_number_states(), state.get_number_actions()))

        for iter in range(max_iters):
            # play the game
            state.init()
            self.play(state)
        return self.qtable

    # PLay the game
    def play(self, state):
        step = 1
        max_steps = 100
        while not state.is_terminal() and step < max_steps:

            # best action to play
            if random.random() < self.epsilon:
                action = random.choice(state.get_actions())
            else:
                state_ID = state.get_state_ID()
                action = np.argmax(self.qtable[state_ID-1, :]) + 1

            # update qtable
            old_state = state.get_state_ID()

            state.do_action(action)    # perform the action
            score = state.get_score()  # get the score given the new state

            new_state = state.get_state_ID()

            self.qtable[old_state-1, action-1] = (1 - self.alfa)*self.qtable[old_state-1, action-1] + \
                                                  self.alfa*(score + self.gamma*np.max(self.qtable[new_state-1, :]))
            step += 1
