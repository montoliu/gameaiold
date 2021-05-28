import random


class AgentOneStep:
    def __init__(self, budget):
        self.budget = budget
        self.count = 0

    def act(self, state):
        actions = state.get_actions()
        l_best_action = []
        best_score = -100

        for action in actions:
            new_state = state.clone()
            new_state.do_action(action)
            new_score = new_state.get_score()
            if new_score > best_score:
                best_score = new_score
                l_best_action = [action]
            elif new_score == best_score:
                l_best_action.append(action)

        return random.choice(l_best_action)
