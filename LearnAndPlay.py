import MazeState
import MazeCoinsState
import RaceState
import SimpleLearning
import QLearning
import random


def learn_game(game_name, agent_name, max_iter_learning):
    state = None
    agent = None
    if game_name == "MAZE":
        state = MazeState.MazeState()
    elif game_name == "MAZECOINS":
        state = MazeCoinsState.MazeCoinsState()
    elif game_name == "RACE":
        state = RaceState.RaceState()

    if agent_name == "SimpleLearning":
        agent = SimpleLearning.SimpleLearning()
    elif agent_name == "QLearning":
        agent = QLearning.QLearning()

    print("------------------------------------")
    print("GAME: " + game_name)
    print("AGENT: " + agent_name)
    print("-> Learning to play <-")
    print("------------------------------------")

    model = agent.learn(state, max_iter_learning)
    return model


def play_game(game_name, agent_name, model):
    state = None
    agent = None
    if game_name == "MAZE":
        state = MazeState.MazeState()
    elif game_name == "MAZECOINS":
        state = MazeCoinsState.MazeCoinsState()
    elif game_name == "RACE":
        state = RaceState.RaceState()

    if agent_name == "SimpleLearning":
        agent = SimpleLearning.SimpleLearning()
    elif agent_name == "QLearning":
        agent = QLearning.QLearning()

    print("------------------------------------")
    print("GAME: " + game_name)
    print("AGENT: " + agent_name)
    print("-> Playing using the learned model <-")
    print("------------------------------------")
    step = 1
    max_steps = 100
    agent.set_model(model)

    while not state.is_terminal() and step < max_steps:
        action = agent.act(state)  # ask the agent for the next action to perform
        state.do_action(action)  # perform the action
        score = state.get_score()  # get the score given the new state

        print("Step:" + str(step) + " Action:" + str(action) + " State:" + str(state) + " Score:" + str(score))
        step += 1

    if state.is_winner():
        print("Player reached the goal.")
    elif state.is_loser():
        print("Player fell into a hole.")
    else:
        print("Player didn't reach the goal in the given steps.")


# Main program
# 1. Select the game to play_game
# 2. Select the agent to be used to obtain the best action to play
# 3. Lear how to play
# 4. Play the game using the learned model
if __name__ == "__main__":
    random.seed(1)

    max_iter_learning = 10000
    do_learning = True

    # 1. Select game
    #game_name = "MAZE"
    #game_name = "RACE"
    game_name = "MAZECOINS"

    # 1. Select agent
    #agent_name = "SimpleLearning"
    agent_name = "QLearning"

    # 3. Lear how to play
    model = learn_game(game_name, agent_name, max_iter_learning)
    print("")
    print(model)

    # 4. Play the game using the learned model
    play_game(game_name, agent_name, model)
