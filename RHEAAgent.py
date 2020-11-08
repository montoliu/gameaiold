import math
import random
import copy
import time
import numpy as np

# Population is greather than 1
class RHEAAgent:
    def __init__(self, budget):
        self.n_individuals = 10     # Number of individuals of the population
        self.n_gens = 5             # Number of elements of each individual
        self.BUDGET = budget/1000   # budget parameter is in ms, self.budget in seconds
        self.n_selected = int(math.ceil(self.n_individuals/2))  # Number of individual that will be selected
        self.n_gens_to_mutate = 1   # Number of gens to be mutated

    def act(self, state):
        t0 = time.time()
        state = state.clone()

        l_individuals = self.get_initial_population(state)
        v_evaluations = np.zeros(self.n_individuals)

        while time.time()-t0 < self.BUDGET:
            for i in range(self.n_individuals):
                v_evaluations[i] = self.evaluate(l_individuals[i], state)
                if time.time()-t0 >= self.BUDGET:
                    break

            if time.time()-t0 >= self.BUDGET:
                break

            l_individuals = self.selection(l_individuals, v_evaluations)
            l_individuals = self.crossover(l_individuals)
            self.mutate(l_individuals, state)

        # Get the first action of the best individual
        best = int(np.argmax(v_evaluations))
        return l_individuals[best][0]

    # --------------------------------------------
    # Get the initial population
    # --------------------------------------------
    def get_initial_population(self, state):
        l_individuals = []
        for i in range(self.n_individuals):
            individual = self.get_random_individual(state)
            l_individuals.append(individual)
        return l_individuals

    # --------------------------------------------
    # Get a random individual
    # --------------------------------------------
    def get_random_individual(self, state):
        individual = np.zeros(self.n_gens)
        valid_actions = state.get_actions()
        for i in range(self.n_gens):
            n = random.randint(0, len(valid_actions)-1)
            individual[i] = valid_actions[n]
        return individual

    # --------------------------------------------
    # Evaluate an individual
    # --------------------------------------------
    def evaluate(self, individual, state):
        st = state.clone()
        for i in range(self.n_gens):
            action = individual[i]
            st.do_action(action)

            if st.is_terminal():
                break

        return st.get_score()

    # --------------------------------------------
    # Selection step. Only the best individuals will survive
    # --------------------------------------------
    def selection(self, l_individuals, v_evaluations):
        idx = np.argsort(-v_evaluations)
        return [l_individuals[i] for i in idx[0:self.n_selected]]

    # --------------------------------------------
    # Crossover step
    # --------------------------------------------
    def crossover(self, l_individuals):
        n_news = self.n_individuals - len(l_individuals)
        for i in range(n_news):
            n1 = random.randint(0, len(l_individuals) - 1)
            n2 = random.randint(0, len(l_individuals) - 1)

            new_individual = self.get_new_individual_by_crossover(l_individuals[n1], l_individuals[n2])
            l_individuals.append(new_individual)
        return l_individuals

    # --------------------------------------------
    # Generate a new individual by using crossover
    # --------------------------------------------
    def get_new_individual_by_crossover(self, v1, v2):
        v_new = np.zeros(self.n_gens)
        turn = 1
        for i in range(self.n_gens):
            if turn == 1:
                v_new[i] = v1[i]
                turn = 2
            else:
                v_new[i] = v2[i]
                turn = 1

        return v_new

    # --------------------------------------------
    # Mutate the population
    # --------------------------------------------
    def mutate(self, l_individuals, state):
        i = 0
        for individual in l_individuals:
            self.mutate_one(individual, state)
            i += 1

    # --------------------------------------------
    # Mutate just one individual
    # --------------------------------------------
    def mutate_one(self, individual, state):
        valid_actions = state.get_actions()
        n_actions = len(valid_actions)
        for i in range(self.n_gens_to_mutate):
            n = random.randint(0, self.n_gens - 1)
            m = random.randint(0, n_actions - 1)
            while valid_actions[m] == individual[n]:
                m = random.randint(0, n_actions - 1)
            individual[n] = valid_actions[m]
