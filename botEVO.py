import copy
import math
import sys
import random


# -------------------------------------------------------------------
# Unit
# -------------------------------------------------------------------
# A class for managing military units
class Unit:
    def __init__(self, unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos, player_id):
        self.player_id = player_id
        self.unit_id = unit_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.life = life
        self.unit_type = unit_type
        self.moving = moving
        self.final_xpos = final_xpos
        self.final_ypos = final_ypos
        self.size = 150               # TODO: unit size is 150 in leagues 1 and 2, but in league 3 it is 75

    # It returns the distance between two units
    def get_distance(self, other_unit):
        return math.sqrt((self.pos_x-other_unit.pos_x)**2 + (self.pos_y-other_unit.pos_y)**2)

    # It returns true when the two units collide
    # Two units collide when the distance is less than size/2
    # The original code is in the Referee.java file at line 1757
    # TODO: Program the same behaviour than in Referee.java
    def collide(self, other_unit):
        return self.get_distance(other_unit) <= self.size / 2

    def is_player_top(self):
        return self.player_id == 0

    def is_player_bottom(self):
        return self.player_id == 1

    def get_size(self):
        return self.size

    def get_direction(self):
        return self.direction

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def set_moving(self, dx, dy):
        if dx > 0 or dy > 0:
            self.moving = 1
        else:
            self.moving = 0

    # Actualize the direction of the motion
    def set_direction(self, dx, dy):
        d = math.degrees(math.atan2(dy, dx))
        if self.is_player_top():
            d += 180
        if d < 0:
            d = 360 + d

        if d < 22.5 or d >= 337.5:
            self.direction = 3
        elif 22.5 <= d < 67.5:
            self.direction = 2
        elif 67.5 <= d < 112.5:
            self.direction = 1
        elif 112.5 <= d < 157.5:
            self.direction = 0
        elif 157.5 <= d < 202.5:
            self.direction = 7
        elif 202.5 <= d < 247.5:
            self.direction = 6
        elif 247.5 <= d < 292.5:
            self.direction = 5
        elif 292.5 <= d < 337.5:
            self.direction = 4

    def is_moving(self):
        return self.moving == 1

    def is_alive(self):
        return self.life > 0

    def get_life(self):
        return self.life

    def get_unit_type_str(self):
        if self.unit_type == 0:
            return "Sword"
        elif self.unit_type == 1:
            return "Spears"
        elif self.unit_type == 2:
            return "Kniqht"
        elif self.unit_type == 3:
            return "Archer"

    def get_direction_str(self):
        if self.direction == 0:
            return "NW"
        elif self.direction == 1:
            return "NO"
        elif self.direction == 2:
            return "NE"
        elif self.direction == 3:
            return "EA"
        elif self.direction == 4:
            return "SE"
        elif self.direction == 5:
            return "SO"
        elif self.direction == 6:
            return "SW"
        elif self.direction == 7:
            return "WE"

    def get_defence(self):
        if self.unit_type == 0:
            return 10
        elif self.unit_type == 1:
            return 20
        elif self.unit_type == 2:
            return 12
        elif self.unit_type == 3:
            return 5

    def get_attack(self):
        if self.unit_type == 0:
            return 20
        elif self.unit_type == 1:
            return 15
        elif self.unit_type == 2:
            return 12
        elif self.unit_type == 3:
            return 10

    def get_speed(self):
        if self.unit_type == 0:
            return 15
        elif self.unit_type == 1:
            return 10
        elif self.unit_type == 2:
            return 40
        elif self.unit_type == 3:
            return 15

    def get_charge_resistence(self):
        if self.unit_type == 0:
            return 25
        elif self.unit_type == 1:
            return 125
        elif self.unit_type == 2:
            return 15
        elif self.unit_type == 3:
            return 0

    def get_charge_force(self):
        if self.unit_type == 0:
            return 5
        elif self.unit_type == 1:
            return 10
        elif self.unit_type == 2:
            return 100
        elif self.unit_type == 3:
            return 5

    def get_arrow_resistence(self):
        if self.unit_type == 0:
            return 10
        elif self.unit_type == 1:
            return 30
        elif self.unit_type == 2:
            return 30
        elif self.unit_type == 3:
            return 10

    def get_arrow_distance(self):
        if self.unit_type == 3:
            return 450
        else:
            return -1

    def get_arrow_damage(self):
        if self.unit_type == 3:
            return 20
        else:
            return -1

    def is_archer(self):
        return self.unit_type == 3

    def in_archer_range(self, other_unit):
        if self.get_distance(other_unit) <= self.get_arrow_distance():
            return True
        else:
            return False

    # def __str__(self):
    #     s = "ID: " + str(self.unit_id) + " " + self.get_unit_type_str() + \
    #         " [" + str(self.pos_x) + ", " + str(self.pos_y) + "] Life: " + str(self.life) + \
    #         " " + self.get_direction_str() + " Moving: " + str(self.moving)
    #     return s

    def __str__(self):
        s = str(self.unit_id) + " " + str(self.pos_x) + " " + str(self.pos_y) + " " + str(self.direction) + " " + \
            str(self.life) + " " + str(self.unit_type) + " " + str(self.moving)
        if self.final_xpos != -1:
            s += " " + str(self.final_xpos) + " " + str(self.final_ypos)
        return s


# -------------------------------------------------------------------
# Micro Action
# -------------------------------------------------------------------
# An action to be played for a single unit
# E.g. 1 50 0;
class MicroAction:
    def __init__(self, unit_id, delta_x, delta_y):
        self.unit_id = unit_id
        self.delta_x = delta_x
        self.delta_y = delta_y

    def __str__(self):
        return str(self.unit_id) + " " + str(self.delta_x) + " " + str(self.delta_y) + ";"


# -------------------------------------------------------------------
# Action
# -------------------------------------------------------------------
# An action is a list of micro actions that will be played in the same turn
# e.g. 1 45 56; 2 40 100; 3 0 0; 4 100 -100
class Action:
    def __init__(self):
        self.l_micro_actions = []

    def add(self, micro_action):
        self.l_micro_actions.append(micro_action)

    # string version of the action
    def __str__(self):
        s = ""
        for micro_action in self.l_micro_actions:
            s += str(micro_action) + " "
        return s


# -------------------------------------------------------------------
# TotalBotWarGame
# -------------------------------------------------------------------
# This is the Game core to play simulations
# The original code is in the Referre.java
class TotalBotWarGame:
    def __init__(self, n_units, state):
        self.n_units = n_units
        self.state = state

    # Moving action
    # Actualize units' positions
    # The original code is in the Referee.java at line 1593
    # TODO: An unit stops when colliding with an enemy
    # TODO: take into account the limits of the battlefield
    # TODO: Actualize units' final position
    # The 0,0 is the top, right corner
    def move(self, new_state, action):
        # for each micro action in action, move it using the unit speed and the direction of the motion
        for ma in action.l_micro_actions:
            unit = new_state.ally[ma.unit_id-1]  # unit_id is 1 to N, python is 0 to N-1
            if unit.is_alive():
                delta_x = ma.delta_x
                delta_y = ma.delta_y

                speed = unit.get_speed()
                pos_x = unit.get_pos_x()
                pos_y = unit.get_pos_y()

                dx = min(abs(delta_x), speed)
                if unit.is_player_top():
                    if delta_x > 0:
                        new_pos_x = pos_x + dx
                    else:
                        new_pos_x = pos_x - dx
                else:
                    if delta_x > 0:
                        new_pos_x = pos_x - dx
                    else:
                        new_pos_x = pos_x + dx

                if new_pos_x <= 0:
                    new_pos_x = 0
                elif new_pos_x >= 1920:
                    new_pos_x = 1919

                dy = min(abs(delta_y), speed)
                if unit.is_player_top():
                    if delta_y > 0:
                        new_pos_y = pos_y + dy
                    else:
                        new_pos_y = pos_y - dy
                else:
                    if delta_y > 0:
                        new_pos_y = pos_y - dy
                    else:
                        new_pos_y = pos_y + dy

                if new_pos_y <= 0:
                    new_pos_y = 0
                elif new_pos_y >= 1080:
                    new_pos_y = 1079

                unit.set_moving(dx, dy)
                unit.set_direction(delta_x, delta_y)
                unit.set_pos(new_pos_x, new_pos_y)

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
                (d1 == 7 and d2 in [2, 3, 4]) or \
                (d1 == 0 and d2 in [3, 4, 5]):
            return 1
        else:
            return 3

    # Figth step between two units.
    # Actualize the life of units
    # Step 1: charge
    # Step 2: normal attack
    # The original code is in the Referee.java file at line 1781
    # TODO: Implement the same behaviour than in Referee
    def fight(self, unit_ally, unit_enemy, enemy_already_fight):
        damage_to_enemy = 0
        damage_to_ally = 0
        # charge if ally is moving
        if unit_ally.is_moving():
            damage_to_enemy = unit_ally.get_charge_force() - \
                              (unit_enemy.get_charge_resistence() / self.charge_factor(unit_ally, unit_enemy))

            if damage_to_enemy < 0:
                damage_to_enemy = 0

        # charge if enemy is moving
        if unit_enemy.is_moving():
            damage_to_ally = unit_enemy.get_charge_force() - \
                             (unit_ally.get_charge_resistence() / self.charge_factor(unit_enemy, unit_ally))

            if damage_to_ally < 0:
                damage_to_ally = 0

        # normal fight ally to enemy
        damage_to_enemy += unit_ally.get_attack() - unit_enemy.get_defence() / 2

        # normal fight enemy to ally
        if not enemy_already_fight:
            damage_to_ally += unit_enemy.get_attack() - unit_ally.get_defence() / 2

        if damage_to_enemy < 0:
            damage_to_enemy = 0

        unit_enemy.life -= damage_to_enemy

        if damage_to_ally < 0:
            damage_to_ally = 0

        unit_enemy.life -= damage_to_ally

    # Archer attack
    # The original code is in the Referee.java file at line 1843
    # TODO: Implement the same behaviour than in Referee
    def archer_attack(self, unit_ally, unit_enemy):
        damage_to_enemy = unit_ally.get_arrow_damage() - unit_enemy.get_arrow_resistence() / 2
        if damage_to_enemy < 0:
            damage_to_enemy = 0

        unit_enemy.life -= damage_to_enemy
        return True

    # There is a combat between two units
    # When two units fight, ally unit produce damage to enemy unit and viceversa.
    # Two ally units can attack to the same enemy unit but the enemy unit produces damage to just one unit
    # if not collide, check archers attack
    # TODO: Implement the same behaviour than in Referee
    def combat(self, new_state):
        enemy_fighting = [False for i in range(new_state.get_number_units())]
        for unit_ally in new_state.ally:
            if unit_ally.is_alive():
                i = 0
                for unit_enemy in new_state.enemy:
                    if unit_enemy.is_alive():
                        if unit_ally.collide(unit_enemy):                            # collide
                            self.fight(unit_ally, unit_enemy, enemy_fighting[i])
                            enemy_fighting[i] = True
                        else:                                                        # not collide, check archers
                            if unit_ally.is_archer() and unit_ally.in_archer_range(unit_enemy):
                                self.archer_attack(unit_ally, unit_enemy)
                            if unit_enemy.is_archer() and not enemy_fighting[i] and unit_enemy.in_archer_range(unit_ally):
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
        self.ally = []        # list of ally units
        self.enemy = []       # list of enemy units

    # returns a hard copy of the object
    # If we change the copy, the original is not modified
    def clone(self):
        new_state = State(self.number_units)
        for u in self.ally:
            new_u = copy.copy(u)
            new_state.ally.append(new_u)
        for u in self.enemy:
            new_u = copy.copy(u)
            new_state.enemy.append(new_u)
        return new_state

    def add_ally(self, unit):
        self.ally.append(unit)

    def add_enemy(self, unit):
        self.enemy.append(unit)

    def get_number_units(self):
        return self.number_units

    def __str__(self):
        s = str(self.number_units) + "\n"
        for unit in self.ally:
            s += str(unit) + "\n"
        for unit in self.enemy:
            s += str(unit) + "\n"
        return s


# -------------------------------------------------------------------
# Heuristic function
# -------------------------------------------------------------------
# Estimate a score given a state
# score = Sum ally life point - sum enemy life points
# The greather, the better
# TODO: Improve heuristic
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
# Evolutionary algorithm
# An individual is a vector of 4 gens (one for ech ally unit)
# A Gen is one of the followings:
#       0 No motion; 1,2,3,4 move to enemy 1,2,3,4; -1,-2,-3,-4 move in opposite direction from enemy 1,2,3,4
class Agent:
    def __init__(self):
        self.number_units = 4
        self.n_iter = 100
        self.population_size = 10   # how many individuals has the population
        self.pct_selection = 0.5    # pct od individual will survie in the selection step
        self.pct_mutation = 0.1     # pct of gens mutated in the mutation step

    # return a random individual
    def get_random_individual(self):
        individual = [0 for i in range(self.number_units)]
        for i in range(len(individual)):
            individual[i] = random.randint(-4, self.number_units)  # random number between -4 and 4
        return individual

    # return the initial population (by random)
    def get_initial_population(self):
        population = []
        for i in range(self.population_size):
            individual = self.get_random_individual()
            population.append(individual)
        return population

    # returns a sub population with the best individuals (according to their scores)
    def selection(self, population, scores):
        sorted_scores = copy.copy(scores)
        sorted_scores.sort()
        cut_idx = math.floor(self.population_size * self.pct_selection)
        cut_score = sorted_scores[cut_idx-1]

        selected_population = []
        i = 0
        n = 0
        for individual in population:
            if scores[i] >= cut_score:
                selected_population.append(individual)
                n += 1
            if n > cut_idx:   # not more than selected
                break
            i += 1

        return selected_population

    # create a new child using to individuals as parents
    # Gens are selected from the parents randomly
    def new_child(self, parent1, parent2):
        individual = [0 for i in range(self.number_units)]

        for i in range(len(individual) - 1):
            parent_id = random.random()
            if parent_id >= 0.5:
                individual[i] = parent1[i]
            else:
                individual[i] = parent2[i]

        return individual

    # Add children using the current population as parents
    def add_children(self, population):
        new_population = []
        for i in range(len(population)):
            new_population.append(population[i])

        num_children = self.population_size - len(population)
        for i in range(num_children):
            # select two parents randomly
            parent1 = random.randint(0,len(population) - 1)
            parent2 = random.randint(0,len(population) - 1)

            child = self.new_child(population[parent1], population[parent2])
            new_population.append(child)
        return new_population

    # mutate individual
    # A pct of the gens are mutated. New gen is selected randomly
    def mutate_individual(self, individual, gens_to_mutate):
        new_individual = copy.copy(individual)
        for i in range(gens_to_mutate):
            idx = random.randint(0, len(individual) - 1)
            new_individual[idx] = random.randint(-4, self.number_units)
        return new_individual

    # Mutate a pct of gens of each indvidual
    def mutate_population(self, population):
        new_population = []
        gens_to_mutate = math.ceil(self.pct_mutation * self.number_units)
        for individual in population:
            new_individual = self.mutate_individual(individual, gens_to_mutate)
            new_population.append(new_individual)
        return new_population

    # get dx, dx to be played
    def get_deltas(self, unit_ally_id, unit_enemy_id, actual_state):
        # look for unit_ally
        for unit in actual_state.ally:
            if unit.unit_id == unit_ally_id:
                unit_ally = unit
                break

        # look for unit_enemy
        for unit in actual_state.enemy:
            if unit.unit_id == abs(unit_enemy_id):
                unit_enemy = unit
                break

        if not unit_enemy.is_alive():
            dx = 0
            dy = 0
        else:
            dx = unit_enemy.get_pos_x() - unit_ally.get_pos_x()
            dy = unit_enemy.get_pos_y() - unit_ally.get_pos_y()

            if unit_enemy_id < 0:
                dx = -dx
                dy = -dy

        return dx, dy

    # Transform an indiividual into an action
    def individual2action(self, individual, actual_state):
        a = Action()
        unit_id = 1
        for gen in individual:
            if not actual_state.ally[unit_id - 1].is_alive():
                ma = MicroAction(unit_id, 0, 0)
            elif gen == 0:
                ma = MicroAction(unit_id, 0, 0)
            elif gen == -4:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == -3:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == -2:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == -1:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == 1:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == 2:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == 3:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)
            elif gen == 4:
                dx, dy = self.get_deltas(unit_id, -4, actual_state)
                ma = MicroAction(unit_id, dx, dy)

            a.add(ma)
            unit_id += 1
        return a

    # returns good good is the action
    def evaluate_individual(self, individual, actual_state, forward_model, heuristic_function):
        action = self.individual2action(individual, actual_state)
        return heuristic_function.get_score(forward_model.play(actual_state, action))

    # evaluate all the individual. Returns the scores
    def evaluate_population(self, population, actual_state, forward_model, heuristic_function):
        scores = []
        for individual in population:
            scores.append(self.evaluate_individual(individual, actual_state, forward_model, heuristic_function))
        return scores

    def act(self, actual_state, forward_model, heuristic_function):
        self.number_units = actual_state.get_number_units()
        population = self.get_initial_population()

        for i in range(self.n_iter):
            scores = self.evaluate_population(population, actual_state, forward_model, heuristic_function)
            population = self.selection(population, scores)
            population = self.add_children(population)
            population = self.mutate_population(population)

        scores = self.evaluate_population(population, actual_state, forward_model, heuristic_function)

        # si no hay de un unico "mejor", seleccionar uno al azar
        idx = 0
        idxs_best_score = [i for i, j in enumerate(scores) if j == max(scores)]
        if len(idxs_best_score) > 1:
            idx = random.randint(0, len(idxs_best_score) - 1)
            idx = idxs_best_score[idx]
        else:
            idx = idxs_best_score[0]

        return self.individual2action(population[idx], actual_state)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# main program
# -------------------------------------------------------------------
# -------------------------------------------------------------------
random.seed(0)       # para hacer debug es mejor dejar este valor costante.
my_agent = Agent()
forward_model = ForwardModel()
heuristic_function = HeuristicFunction()

number_units = int(input())  # How many troops are on each side.

# game loop
while True:
    st = State(number_units)
    # player 0 (top of the battlefield)
    for i in range(number_units):
        player_id = 0
        unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos = [int(j) for j in input().split()]
        u = Unit(unit_id, pos_x, pos_y, direction, life, unit_type, moving, final_xpos, final_ypos, player_id)
        st.add_ally(u)

    # player 1 (bottom of the battlefield)
    for i in range(number_units):
        player_id = 1
        unit_id, pos_x, pos_y, direction, life, unit_type, moving = [int(j) for j in input().split()]
        u = Unit(unit_id, pos_x, pos_y, direction, life, unit_type, moving, -1, -1, player_id)
        st.add_enemy(u)

    print(str(st))

    action = my_agent.act(st, forward_model, heuristic_function)


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)