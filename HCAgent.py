import random
import copy
import numpy as np
import time

# Population is always 1
# At each step, the individual is tested against a mutated version of itself. The best of the two is the new individual
class HCAgent:
    def __init__(self, budget):
        self.n_gens = 5            # Number of gens of the individual
        self.BUDGET = budget/1000  # budget parameter is in ms, self.budget in seconds
        self.n_gens_to_mutate = 1  # number of gens to mutate

    def act(self, state):
        t0 = time.time()       # initial time
        state = state.clone()

        org_individual = self.get_random_individual(state)   # The first individual is random
        score1 = self.evaluate(org_individual, state)        # Get the score of the first individual

        while time.time()-t0 < self.BUDGET:
            new_individual = self.mutate(org_individual, state)  # Mutate the actual individual
            score2 = self.evaluate(new_individual, state)        # Get the score of the mutated individual
            if score2 >= score1:                                 # which is the best?
                org_individual = new_individual
                score1 = score2

        return org_individual[0]  # return the first action of the best individual at the end of the process

    # ---------------------------------------------
    # Return a random individual
    # ---------------------------------------------
    def get_random_individual(self, state):
        individual = np.zeros(self.n_gens)
        valid_actions = state.get_actions()
        for i in range(self.n_gens):
            n = random.randint(0, len(valid_actions)-1)
            individual[i] = valid_actions[n]
        return individual

    # ---------------------------------------------
    # Return the score of an individual starting from a state
    # ---------------------------------------------
    def evaluate(self, individual, state):
        st = state.clone()
        for i in range(self.n_gens):
            action = individual[i]
            st.do_action(action)

            if st.is_terminal():
                break

        return st.get_score()

    # ---------------------------------------------
    # Mutate an individual
    # ---------------------------------------------
    def mutate(self, individual, state):
        new_individual = copy.copy(individual)
        valid_actions = state.get_actions()
        n_actions = len(valid_actions)
        for i in range(self.n_gens_to_mutate):
            n = random.randint(0, self.n_gens - 1)     # The gen to mutate
            m = random.randint(0, n_actions - 1)       # The action to insert in the gen
            while valid_actions[m] == individual[n]:   # if the new action is equal to the previous one ...
                m = random.randint(0, n_actions - 1)

            new_individual[n] = valid_actions[m]       # Replace the action

        return new_individual
