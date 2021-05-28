import random


class AgentRandom:
    def act(self, state):
        actions = state.get_actions()
        return random.choice(actions)
