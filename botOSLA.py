import copy
import math


# -------------------------------------------------------------------
# Unit
# -------------------------------------------------------------------
# A class for managing military units
class Unit:
    def __init__(self, unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos):
        self.unit_id = unit_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.life = life
        self.unit_type, = unit_type
        self.moving = moving
        self.final_xpos = final_xpos
        self.final_ypos = final_ypos

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y

    def is_moving(self):
        return self.moving == 1

    def is_alive(self):
        return self.life > 0

    def get_life(self):
        return self.life

    def get_defence(self):
        if self.unit_type == 1:
            return 10
        elif self.unit_type == 2:
            return 20
        elif self.unit_type == 3:
            return 12
        elif self.unit_type == 4:
            return 5

    def get_attack(self):
        if self.unit_type == 1:
            return 20
        elif self.unit_type == 2:
            return 15
        elif self.unit_type == 3:
            return 12
        elif self.unit_type == 4:
            return 10

    def get_speed(self):
        if self.unit_type == 1:
            return 15
        elif self.unit_type == 2:
            return 10
        elif self.unit_type == 3:
            return 40
        elif self.unit_type == 4:
            return 15

    def get_charge_resistence(self):
        if self.unit_type == 1:
            return 25
        elif self.unit_type == 2:
            return 125
        elif self.unit_type == 3:
            return 15
        elif self.unit_type == 4:
            return 0

    def get_charge_force(self):
        if self.unit_type == 1:
            return 5
        elif self.unit_type == 2:
            return 10
        elif self.unit_type == 3:
            return 100
        elif self.unit_type == 4:
            return 5

    def get_arrow_resistence(self):
        if self.unit_type == 1:
            return 10
        elif self.unit_type == 2:
            return 30
        elif self.unit_type == 3:
            return 30
        elif self.unit_type == 4:
            return 10

    def get_arrow_distance(self):
        if self.unit_type == 4:
            return 450
        else:
            return -1

    def get_arrow_damage(self):
        if self.unit_type == 4:
            return 20
        else:
            return -1


# -------------------------------------------------------------------
# TotalBotWarGame
# -------------------------------------------------------------------
# This is the Game core to play simulations
class TotalBotWarGame:
    def __init__(self, n_units, state):
        self.n_units = n_units
        self.state = state

    def move(self, new_state, action):
        for ma in action.l_micro_actions:
            speed = new_state.ally[ma.unit_id].get_speed()
            pos_x = new_state.ally[ma.unit_id].get_pos_x()
            pos_y = new_state.ally[ma.unit_id].get_pos_y()
            delta_x = ma.delta_x
            delta_y = ma.delta_y

            dx = min(abs(delta_x), speed)
            if delta_x > 0:
                new_pos_x = pos_x + dx
            else:
                new_pos_x = pos_x - dx

            dy = min(abs(delta_y), speed)
            if delta_y > 0:
                new_pos_y = pos_y + dy
            else:
                new_pos_y = pos_y - dy

            new_state.ally[ma.unit_id].set_pos_x(new_pos_x)
            new_state.ally[ma.unit_id].set_pos_y(new_pos_y)

    def combat(self, new_state):
        return

    def play(self, action):
        new_state = self.state.clone()
        self.move(new_state, action)
        self.combat(new_state)
        return new_state


# -------------------------------------------------------------------
# Micro Action
# -------------------------------------------------------------------
# An action to played for a single unit
class MicroAction:
    def __init__(self, unit_id, delta_x, delta_y):
        self.unit_id = unit_id
        self.delta_x = delta_x
        self.delta_y = delta_y

    def to_str(self):
        return str(self.unit_id) + " " + str(self.delta_x) + " " + str(self.delta_y) + ";"


# -------------------------------------------------------------------
# Action
# -------------------------------------------------------------------
# An action is a list of micro actions that will be played in the same turn
class Action:
    def __init__(self):
        self.l_micro_actions = []

    def add(self, micro_action):
        self.l_micro_actions.append(micro_action)

    def to_str(self):
        action = ""
        for micro_action in self.l_micro_actions:
            action += micro_action.to_str()
        return action


# -------------------------------------------------------------------
# State
# -------------------------------------------------------------------
# The state of the game
class State:
    def __init__(self, n):
        self.number_units = n
        self.ally = []
        self.enemy = []

    # return a copy of the object
    # If we change the copy, the original is not modified
    def clone(self):
        new_state = State(self.number_units)
        new_state.ally = copy.copy(self.ally)
        new_state.enemy = copy.copy(self.enemy)
        return new_state

    def add_ally(self, unit):
        self.ally.append(unit)

    def add_enemy(self, unit):
        self.enemy.append(unit)

    # return list with all the possible actions that can be played given the state
    # TODO: Pensar en otra forma de obtener las acciones
    def get_all_possible_actions(self):
        ma1_1 = MicroAction(1, 0, 100)
        ma1_2 = MicroAction(2, 0, -100)
        ma1_3 = MicroAction(3, 100, 0)
        ma1_4 = MicroAction(4, -100, 0)
        a1 = Action()
        a1.add(ma1_1)
        a1.add(ma1_2)
        a1.add(ma1_3)
        a1.add(ma1_4)

        ma2_1 = MicroAction(1, 0, 100)
        ma2_2 = MicroAction(2, 0, -100)
        ma2_3 = MicroAction(3, 100, 0)
        ma2_4 = MicroAction(4,-100, 0)
        a2 = Action()
        a2.add(ma2_1)
        a2.add(ma2_2)
        a2.add(ma2_3)
        a2.add(ma2_4)

        l_actions = [a1, a2]
        return l_actions


# -------------------------------------------------------------------
# Heuristic function
# -------------------------------------------------------------------
# Estimate a score given a state
# score = Sum ally life point - sum enemy life points
# The greather, the better
# TODO: pensar en heurísticas alternativas
class HeuristicFunction:
    def get_score(self, state):
        ally = 0
        enemy = 0
        for i in range(state.number_units):
            ally += state.ally[i].get_life()
            enemy += state.enemy[i].get_life()

        return ally - enemy


# -------------------------------------------------------------------
# Forward Model
# -------------------------------------------------------------------
# Given a state and an action, play the action and return the resulting state
class ForwardModel:
    def play(self, state, action):
        game = TotalBotWarGame(state.number_units, state)
        new_state = game.play(action)
        return new_state


# -------------------------------------------------------------------
# Agent
# -------------------------------------------------------------------
# One Steep Look Ahead algorithm
# For each action that can be played, play the action and get the score
# The action with the best score is the one selected
class Agent:
    def act(self, actual_state, forward_model, heuristic_function):
        l_actions = actual_state.get_all_possible_actions()
        best_action = l_actions[0]
        best_score = 0

        for action in l_actions:
            new_state = forward_model.play(actual_state, action)
            score = heuristic_function.get_score(new_state)
            if score > best_score:
                best_score = score
                best_action = action

        action = best_action.to_str()
        return action


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# main program
# -------------------------------------------------------------------
# -------------------------------------------------------------------
my_agent = Agent()
forward_model = ForwardModel()
heuristic_function = HeuristicFunction()

number_units = int(input())  # How many troops are on each side.

# game loop
while True:
    st = State(number_units)
    for i in range(number_units):
        unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos = [int(j) for j in input().split()]
        u = Unit(unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos)
        st.add_ally(u)
    
    for i in range(number_units):
        unit_id, pos_x, pos_y, direction, life, unit_type, moving = [int(j) for j in input().split()]
        u = Unit(unit_id, pos_x, pos_y, direction, life, unit_type, moving, -1, -1)
        st.add_enemy(u)

    action = my_agent.act(st, forward_model, heuristic_function)
    print(action)


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
