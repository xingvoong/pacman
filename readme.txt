- foundational AI concepts, such as informed state-space search, probabilistic inference, 
and reinforcement learning through the game Pacman.

-Pacman 1:
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
-Pacman 2: 
	- Pacman world is modeled as both an adversarial and a stochastic search problem, still the Pacman, 
		but include ghosts now.
	- Main file: multiAgents.py:  multi-agent search agents
	- Implemented both minimax and expectimax search.
	- A new evaluation:
		-the distance from the pacmac new position to the foods
		- 1/distance as a new heuristic
	

