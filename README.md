# Pacman
Foundational AI concepts, such as informed state-space search, probabilistic inference, and reinforcement learning through the game Pacman.
## Features

- **Pacman 1:**
	- Helped Pacman find paths through it maze world, 
		both to reach a particular location and to collect food efficiently

	- Main files: search.py: search algorithms.
	      searchAgents.py:  search-based agents.

	- Search algorithms:
		Depth First Search
		Breadth First Search
		Uniform Cost Search
		A*
	- Heuristic: Euclidean distance and Manhattan distance.
- **Pacman 2:** 
	- Pacman world is modeled as both an adversarial and a stochastic search problem, still the Pacman, 
		but include ghosts now.
	- Main file: multiAgents.py:  multi-agent search agents
	- Implemented both minimax and expectimax search.
	- A new evaluation:
		-the distance from the pacmac new position to the foods
		- 1/distance as a new heuristic
- **Pacman 3:**
	- Implemented model-based and model-free reinforcement learning algorithms; value iteration and Q-learning. 
	- Tested the agents first on Gridworld (from class)
	- Then apply them to a simulated robot controller (Crawler) and Pacman.
	- Main files:
		valueIterationAgents.py: A value iteration agent for solving known MDPs.
		qlearningAgents.py: Q-learning agents for Gridworld, Crawler and Pacman.
- **Pacman 4:**
	- Probabilistic inference in a hidden Markov model tracks the movement of hidden ghosts in the Pacman world.
	- Implemented exact inference using the forward algorithm and approximate inference via particle filters.
	- Pacman agents that use sensors to locate and eat invisible ghosts
	- Advanced from locating single, stationary ghosts 
		to hunting packs of multiple moving ghosts with ruthless efficiency.
	- Main file: 
		bustersAgents.py:  Agents for playing the Ghostbusters variant of Pacman.
		inference.py: Code for tracking ghosts over time using their sounds.

## Acknowledgements
- [UC Berkeley CS188](https://inst.eecs.berkeley.edu/~cs188)
