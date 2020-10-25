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
        self.size = 150

    def get_distance(self, other_unit):
        return math.sqrt((self.pos_x-other_unit.pos_x)**2 + (self.pos_y-other_unit.pos_y)**2)

    # Returns true when the two units collide
    # Two units collide when the distance is less than size/2
    # The original code is in the Referee.java file at line 1757
    # TODO: Program the same behaviour than in Referee.java
    def collide(self, other_unit):
        return self.get_distance(other_unit) <= self.size / 2

    def get_size(self):
        return self.size

    def get_direction(self):
        return self.direction

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

    def is_archer(self):
        return self.unit_type == 4

    def in_archer_range(self, other_unit):
        if self.get_distance(other_unit) <= self.get_arrow_distance():
            return True
        else:
            return False


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
# TotalBotWarGame
# -------------------------------------------------------------------
# This is the Game core to play simulations
# The original code is in the Referre.java
class TotalBotWarGame:
    def __init__(self, n_units, state):
        self.n_units = n_units
        self.state = state

    # moving action
    # Actualize units' positions
    # The original code is in the Referre.java at line 1593
    # TODO: An unit stops when colliding with an enemy
    # TODO: take into account the limits of the battleground
    # TODO: Actualize units' moving direction
    # TODO: Actualize units' is moving
    # TODO: Actualize units' final position
    def move(self, new_state, action):
        # for each micro action in action, move it using the unit speed and the direction of the motion
        for ma in action.l_micro_actions:
            unit = new_state.ally[ma.unit_id]
            delta_x = ma.delta_x
            delta_y = ma.delta_y

            speed = unit.get_speed()
            pos_x = unit.get_pos_x()
            pos_y = unit.get_pos_y()

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

            unit.set_pos_x(new_pos_x)
            unit.set_pos_y(new_pos_y)

    # Frontal charge u1 to u2 returns 1.0
    # Other returns 3.0
    # Directions: NorthWest 0, North 1, ..., west 7
    # The original code is in the Referee.java file at line 1833
    # TODO: Implement the same behaviour than in Referee
    def charge_factor(self, unit1, unit2):
        d1 = unit1.get_direction()
        d2 = unit2.get_direction()
        if (d1 == 1 and d2 in [4, 5, 6]) or \
                (d1 == 2 and d2 in [5, 6, 7]) or \
                (d1 == 3 and d2 in [6, 7, 0]) or \
                (d1 == 4 and d2 in [7, 0, 1]) or \
                (d1 == 5 and d2 in [0, 1, 2]) or \
                (d1 == 6 and d2 in [1, 2, 3]) or \
                (d1 == 6 and d2 in [2, 3, 4]) or \
                (d1 == 0 and d2 in [3, 4, 5]):
            return 1
        else:
            return 3

    # Figth step between two units.
    # Actualize the life of units
    # Step 1: charge
    # Step 2: normal attack
    # The original code is in the Referee.java file at line 1781
    def fight(self, unit_ally, unit_enemy, enemy_already_fight):
        damage_to_enemy = 0
        damate_to_ally = 0
        # charge if ally is moving
        if unit_ally.is_moving():
            damage_to_enemy = unit_ally.get_charge_force() - (unit_enemy.get_charge_resistence() / self.charge_factor(unit_ally, unit_enemy))

        # charge if enemy is moving
        if unit_enemy.is_moving():
            damate_to_ally = unit_enemy.get_charge_force() - (unit_ally.get_charge_resistence() / self.charge_factor(unit_enemy, unit_ally))

        # normal fight ally to enemy
        damage_to_enemy += unit_ally.get_attack - unit_enemy.get_defence() / 2

        # normal fight enemy to ally
        if not enemy_already_fight:
            damate_to_ally += unit_enemy.get_attack - unit_ally.get_defence() / 2

        if damage_to_enemy < 0:
            damage_to_enemy = 0

        unit_enemy.life -= damage_to_enemy

        if damate_to_ally < 0:
            damate_to_ally = 0
        unit_enemy.life -= damate_to_ally

    # Archer attack
    # The original code is in the Referee.java file at line 1843
    def archer_attack(self, unit_ally, unit_enemy):
        damage_to_enemy = unit_ally.get_arrow_damage - unit_enemy.get_arrow_resistence() / 2
        if damage_to_enemy < 0:
            damage_to_enemy = 0

        unit_enemy.life -= damage_to_enemy
        return True

    # There is a combat between two units
    # When two units fight, ally unit produce damage to enemy unit and viceversa.
    # Two ally units can attack to the same enemy unit but the enemy unit produces damage to just one unit
    # if not collide, check archers attack
    def combat(self, new_state):
        enemy_fighting = [False, False, False, False]  # TODO: for any number of units
        for unit_ally in new_state.ally:
            i = 0
            for unit_enemy in new_state.enemy:
                if unit_ally.collide(unit_enemy):
                    self.fight(unit_ally, unit_enemy, enemy_fighting[i])
                    enemy_fighting[i] = True
                else:
                    if unit_ally.is_archer() and unit_ally.in_archer_range(unit_enemy):
                        self.archer_attack(unit_ally, unit_enemy)
                    if unit_enemy.is_archer() and unit_enemy.in_archer_range(unit_ally):
                        self.archer_attack(unit_enemy, unit_ally)
                        enemy_fighting[i] = True
                i += 1

    # Play a turn
    # Step 1: Move units
    # Step 2: combat
    def play(self, action):
        new_state = self.state.clone()
        self.move(new_state, action)
        self.combat(new_state)
        return new_state


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

        ma2_1 = MicroAction(1, 0, -100)
        ma2_2 = MicroAction(2, 0, 100)
        ma2_3 = MicroAction(3, 100, 50)
        ma2_4 = MicroAction(4, -100, -50)
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
