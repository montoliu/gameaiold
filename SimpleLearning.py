import numpy as np
import random


class SimpleLearning:
    def __init__(self):
        self.qtable = None

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
            l_states_actions, win = self.play(state)
            if win == 1:
                self.update_qtable_positive(l_states_actions)
            else:
                self.update_qtable_negative(l_states_actions)

        return self.qtable

    # PLay the game
    def play(self, state):
        step = 1
        max_steps = 100
        l_states_actions = []
        win = 0
        while not state.is_terminal() and step < max_steps:
            action = random.choice(state.get_actions())
            l_states_actions.append([state.get_state_ID(), action])
            state.do_action(action)  # perform the action
            score = state.get_score()  # get the score given the new state
            if score == 1:
                win = 1
                break
            elif score == -1:
                win = -1
                break
            step += 1

        return l_states_actions, win

    # update the qtable with positive actions
    def update_qtable_positive(self, l_states_actions):
        for state_action in l_states_actions:
            state_number = state_action[0]
            action_number = state_action[1]

            self.qtable[state_number - 1, action_number - 1] += 1

    # update the qtable with negative actions
    def update_qtable_negative(self, l_states_actions):
        for state_action in l_states_actions:
            state_number = state_action[0]
            action_number = state_action[1]

            self.qtable[state_number - 1, action_number - 1] -= 1
