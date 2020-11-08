# --------------------------------
# 5x4 Maze.
# Actions: 1 UP, 2 RIGHT,  3 DOWN, 4 LEFT
# Hole in states: 7, 9, 12 and 18
# Goal in state: 20
# Starting in state: 1
# States:
#  1  2  3  4
#  5  6  7  8
#  9 10 11 12
# 13 14 15 16
# 17 18 19 20
# --------------------------------
import math


class MazeState:
    def __init__(self):
        self.state = 1
        self.GOALS = [20]
        self.HOLES = [7, 9, 12, 18]
        self.TERMINAL = self.HOLES + self.GOALS
        self.SUCCESS = 1
        self.FAIL = -1

    def clone(self):
        st = MazeState()
        st.state = self.state
        return st

    def do_action(self, action):
        if action == 1 and self.state > 4:
            self.state -= 4
        elif action == 3 and self.state < 17:
            self.state += 4
        elif action == 2 and self.state not in [4, 8, 12, 16, 20]:
            self.state += 1
        elif action == 4 and self.state not in [1, 5, 9, 13, 17]:
            self.state -= 1

    def is_terminal(self):
        return self.state in self.TERMINAL

    def get_actions(self):
        if self.is_terminal():
            return []
        return [1, 2, 3, 4]

    # For each non-terminal state return a reward relared to the distance to the goal
    # def get_score(self):
    #     if self.state in self.GOALS:
    #         return self.SUCCESS
    #     elif self.state in self.HOLES:
    #         return self.FAIL
    #     else:
    #         row = math.floor((self.state - 1) / 4) + 1
    #         col = ((self.state - 1) % 4) + 1
    #         distance = math.sqrt((5 - row) ** 2 + (4 - col) ** 2)
    #         return (5 - distance)/5

    # Goal SUCCESS, Holes FAIL, non-terminal 0
    def get_score(self):
        if self.state in self.GOALS:
            return self.SUCCESS
        elif self.state in self.HOLES:
            return self.FAIL
        else:
            return 0

    def __repr__(self):
        return str(self.state)

    # Return the total number of actions
    def get_number_actions(self):
        return 4

    # Return the total number of states
    def get_number_states(self):
        return 20

    # Return the state ID
    def get_state_ID(self):
        return self.state

    def init(self):
        self.state = 1
