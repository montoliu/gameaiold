# Games
import MazeState
import RaceState
# Agents
import RandomAgent
import OneStepAgent
import RHEAAgent
import HCAgent
import MCTSAgent


def play_game(game_name, agent_name, max_steps, budget):
    step = 1
    win = 0

    state = None
    if game_name == "MAZE":
        state = MazeState.MazeState()
    elif game_name == "RACE":
        state = RaceState.RaceState()

    agent = None
    if agent_name == "Random":
        agent = RandomAgent.RandomAgent()
    elif agent_name == "OneStep":
        agent = OneStepAgent.OneStepAgent(budget)
    elif agent_name == "RHEA":
        agent = RHEAAgent.RHEAAgent(budget)
    elif agent_name == "HC":
        agent = HCAgent.HCAgent(budget)
    elif agent_name == "MCTS":
        agent = MCTSAgent.MCTSAgent(budget)

    print("------------------------------------")
    print("GAME: " + game_name)
    print("AGENT: " + agent_name)
    print("------------------------------------")

    while not state.is_terminal() and step < max_steps:
        action = agent.act(state=state)  # ask the agent for the next action to perform
        state.do_action(action)  # perform the action
        score = state.get_score()  # get the score given the new state

        print("Step:" + str(step) + " Action:" + str(action) + " State:" + str(state) + " Score:" + str(score))

        if score == 1:
            win = 1
            break
        elif score == -1:
            win = -1
            break
        step += 1

    if win == 1:
        print("The player gets the goal.")
    elif win == -1:
        print("The player fall in a hole.")
    else:
        print("The player not reach the goal in the given steps.")


if __name__ == "__main__":
    max_steps = 100
    budget = 1000       # 1000 ms -> 1 second

    # Select game
    #game_name = "MAZE"
    game_name = "RACE"

    # Select agent algorithm
    #agent_name = "Random"
    #agent_name = "OneStep"
    #agent_name = "HC"
    #agent_name = "RHEA"
    agent_name = "MCTS"

    play_game(game_name, agent_name, max_steps, budget)

