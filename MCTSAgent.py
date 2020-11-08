import random
import math
import time


class Node:
    def __init__(self, parent, state, action, id):
        self.id = id  # it helps when debugging
        self.parent = parent
        self.state = state
        self.action = action
        self.l_children = []
        self.score = 0
        self.n = 0
        self.C = math.sqrt(2)
        self.BIG_NUMBER = 10E6

    # --------------------------------------------
    # Return the child with best ucb1
    # --------------------------------------------
    def get_best_child(self):
        best_child = None
        best_ucb = -math.inf
        for child in self.l_children:
            epsilon = random.random()/1000.0  # small number. It is used to have small differences in the ucb1
            if child.n == 0:  # not yet visited
                ucb_child = self.BIG_NUMBER + epsilon
            else:
                ucb_child = child.score / child.n + self.C * math.sqrt(math.log(self.n) / child.n) + epsilon
            if ucb_child >= best_ucb:
                best_child = child
                best_ucb = ucb_child

        return best_child


class MCTSAgent:
    def __init__(self, budget):
        self.budget = budget / 1000  # budget is in ms, self.budget in seconds
        self.count = 0
        self.n_nodes = 0

    # --------------------------------------------
    # Return the best action to play
    # --------------------------------------------
    def act(self, state):
        t0 = time.time()
        self.count = 0
        self.n_nodes += 1
        root_node = Node(None, state=state, action=None, id=self.n_nodes)
        self.extend_node(root_node)
        self.rollout_one_random_child(root_node)

        # main loop
        actual_node = root_node
        while time.time()-t0 < self.budget:
            child = actual_node.get_best_child()  # Get the next child to be visited

            if child.n == 0 or child.state.is_terminal():  # not yet visited (or terminal) -> rollout
                score = self.rollout(child)
                child.score += score
                child.n += 1
                self.backpropagation(child.parent, score)
                actual_node = root_node
            elif len(child.l_children) == 0:                # visited without children
                self.extend_node(child)
                self.rollout_one_random_child(child)
                actual_node = root_node
            else:                                           # if it has children, continue traversing the tree
                actual_node = child

        recommend_child = self.recommend_child(root_node)
        return recommend_child.action

    # --------------------------------
    # Return the action corresponding to the best child of the root_node
    # --------------------------------
    def recommend_child(self, root_node):
        best_child = None
        best_score = -math.inf
        for child in root_node.l_children:
            score = child.score / child.n
            if score >= best_score:
                best_score = score
                best_child = child
        return best_child

    # --------------------------------
    # Backpropagation
    # --------------------------------
    def backpropagation(self, node, score):
        while node is not None:
            node.n += 1
            node.score += score
            node = node.parent

    # --------------------------------
    # Simulate the game until a non terminal node is reached
    # --------------------------------
    def rollout(self, node):
        new_state = node.state.clone()

        while not new_state.is_terminal():
            action = random.choice(new_state.get_actions())
            new_state.do_action(action)
            self.count += 1
        score = new_state.get_score()
        return score

    # --------------------------------
    # Randomly select one child to perform the rollout
    # --------------------------------
    def rollout_one_random_child(self, node):
        # Rollout just one random child
        one_child = random.choice(node.l_children)
        score = self.rollout(one_child)

        one_child.score += score
        one_child.n += 1

        self.backpropagation(node, one_child.score)

    # --------------------------------
    # Extend node
    # Create a child for every possible action (only if the state changes).
    # Not add if the resulting state is the same than the parent. This is to prevent a->b->a
    # --------------------------------
    def extend_node(self, node):
        l_actions = node.state.get_actions()

        for action in l_actions:
            new_state = node.state.clone()
            new_state.do_action(action)
            self.count += 1

            if new_state.state != node.state.state and \
                (node.parent is None or (node.parent is not None and new_state.state != node.parent.state.state)):
                self.n_nodes += 1
                new_node = Node(node, new_state, action, id=self.n_nodes)
                node.l_children.append(new_node)
