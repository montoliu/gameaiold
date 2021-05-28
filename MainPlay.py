import random

# Games
import GameMazeState
import GameRaceState
# Agents
import AgentRandom
import AgentOneStep
import AgentRHEA
import AgentHC
import AgentMCTS


# Play a game using an agent
def play_game(game_name, agent_name, max_steps, budget):
    step = 1

    state = None
    if game_name == "MAZE":
        state = GameMazeState.GameMazeState()
    elif game_name == "RACE":
        state = GameRaceState.GameRaceState()

    agent = None
    if agent_name == "Random":
        agent = AgentRandom.AgentRandom()
    elif agent_name == "OneStep":
        agent = AgentOneStep.AgentOneStep(budget)
    elif agent_name == "RHEA":
        agent = AgentRHEA.AgentRHEA(budget)
    elif agent_name == "HC":
        agent = AgentHC.AgentHC(budget)
    elif agent_name == "MCTS":
        agent = AgentMCTS.AgentMCTS(budget)

    print("------------------------------------")
    print("GAME: " + game_name)
    print("AGENT: " + agent_name)
    print("------------------------------------")

    while not state.is_terminal() and step < max_steps:
        action = agent.act(state=state)  # ask the agent for the next action to perform
        state.do_action(action)  # perform the action
        score = state.get_score()  # get the score given the new state

        print("Step:" + str(step) + " Action:" + str(action) + " State:" + str(state) + " Score:" + str(score))

        if state.is_winner():
            print("Player reached the goal.")
            break
        elif state.is_loser():
            print("Player fell into a hole.")
            break
        step += 1

    if step >= max_steps:
        print("Player didn't reach the goal in the given steps.")


# Main program
# 1. Select the game to play_game
# 2. Select the agent to be used to obtain the best action to play
# 3. Play the game
if __name__ == "__main__":
    random.seed()
    max_steps = 100
    budget =500    # 1000 ms -> 1 second

    # 1. Select game
    #game_name = "MAZE"
    game_name = "RACE"

    # 2. Select agent algorithm
    #agent_name = "Random"
    #agent_name = "OneStep"
    #agent_name = "HC"
    agent_name = "RHEA"
    #agent_name = "MCTS"

    # 3. play the game
    play_game(game_name, agent_name, max_steps, budget)

