# --------------------------------
# 20x5 Race.
# Actions: 1 LEFT, 2 STRAIGHT, 3 RIGHT
# Hole in [1,0], [1,1], [2, 4], [2, 5], [3, 4], [3, 5], etc.
# Goal in row: [0, any]
# Starting in state: [19, 2]
# --------------------------------
import copy


class RaceState:
    def __init__(self):
        self.NC = 5
        self.NR = 20
        self.state = [self.NR - 1, 2]
        self.GOALS = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]  # first row
        self.HOLES = self.set_holes()
        self.TERMINAL = self.HOLES + self.GOALS
        self.SUCCESS = 1
        self.FAIL = -1

    def set_holes(self):
        h1 = [[16, 0], [16, 1], [16, 2], [17, 0], [17, 1], [17, 2]]
        h2 = [[12, 2], [12, 3], [12, 4], [13, 2], [13, 3], [13, 4]]
        h3 = [[6, 0], [7, 0], [8, 0]]
        h4 = [[5, 3], [5, 4], [6, 3], [6, 4], [7, 3], [7, 4]]
        h5 = [[2, 3], [2, 4], [3, 3], [3, 4]]
        h6 = [[1, 0], [1, 1]]

        return h1 + h2 + h3 + h4 + h5 + h6

    def clone(self):
        st = RaceState()
        st.state = copy.copy(self.state)
        return st

    def do_action(self, action):
        self.state[0] -= 1
        if action == 1 and self.state[1] > 0:
            self.state[1] -= 1
        elif action == 3 and self.state[1] < self.NC - 1:
            self.state[1] += 1

    def is_terminal(self):
        return self.state in self.TERMINAL

    def get_actions(self):
        if self.is_terminal():
            return []
        return [1, 2, 3]

    # For each non-terminal state return a reward relared to the distance to the goal
    # def get_score(self):
    #     if self.state in self.GOALS:
    #         return self.SUCCESS
    #     elif self.state in self.HOLES:
    #         return self.FAIL
    #     else:
    #         return (self.NR - self.state[0])/self.NR

    # Goal SUCCESS, Holes FAIL, non-terminal 0
    def get_score(self):
        if self.state in self.GOALS:
            return self.SUCCESS
        elif self.state in self.HOLES:
            return self.FAIL
        else:
            return 0

    def __repr__(self):
        s = "[" + str(self.state[0]) + ", " + str(self.state[1]) + "]"
        return s

    # Return the total number of actions
    def get_number_actions(self):
        return 3

    # Return the total number of states
    def get_number_states(self):
        return self.NR * self.NC

    # Return the state ID
    def get_state_ID(self):
        return (self.NR-self.state[0]-1)*self.NC + self.state[1] + 1

    def init(self):
        self.state = [self.NR-1, 2]

    def is_winner(self):
        return self.state in self.GOALS

    def is_loser(self):
        return self.state in self.HOLES
