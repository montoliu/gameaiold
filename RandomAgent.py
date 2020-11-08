import random


class RandomAgent:
    def act(self, state):
        actions = state.get_actions()
        return random.choice(actions)
