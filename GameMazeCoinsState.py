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
import copy


class GameMazeCoinsState:
    def __init__(self):
        self.state = 1
        self.GOALS = [20]
        self.HOLES = [7, 9, 12, 18]
        self.COINS = [11, 13]
        self.TERMINAL = self.HOLES + self.GOALS
        self.SUCCESS = 1
        self.FAIL = -1
        self.COIN_POINTS = 1
        self.points = 0

    def clone(self):
        st = GameMazeCoinsState()
        st.state = self.state
        st.points = self.points
        st.COINS = copy.copy(self.COINS)
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

        if self.state in self.COINS:
            self.points += self.COIN_POINTS
            self.COINS.remove(self.state)

    def is_terminal(self):
        return self.state in self.TERMINAL

    def get_actions(self):
        if self.is_terminal():
            return []

        if self.state == 1:
            return [2, 3]
        elif self.state == 4:
            return [3, 4]
        elif self.state == 17:
            return [1, 2]
        elif self.state == 20:
            return [1, 4]
        elif self.state in [2, 3]:
            return [2, 3, 4]
        elif self.state in [18, 19]:
            return [1, 2, 4]
        elif self.state in [5, 9, 13]:
            return [1, 2, 3]
        elif self.state in [8, 12, 16]:
            return [1, 3, 4]

        return [1, 2, 3, 4]

    # Goal SUCCESS, Holes FAIL, non-terminal 0
    def get_score(self):
        if self.state in self.GOALS:
            return self.SUCCESS + self.points
        elif self.state in self.HOLES:
            return self.FAIL + self.points
        else:
            return self.points

    def is_winner(self):
        return self.state in self.GOALS

    def is_loser(self):
        return self.state in self.HOLES

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
