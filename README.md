# WELCOME TO PACMAN - AI!
SofDes Spring'15 final project by Kelly Brennan, Stephanie Northway, and Pinar Demetci.
The project aims to use AI and machine learning strategies for pathfinding in PacMan. 

**What is PacMan-AI?**
It's a class project we took on to teach ourselves about AI, specifically reinforcement learning, and even more specifically Q-learning. It's a Pacman game that plays itself and learns from its experience. Each time it makes a move, it updates the weights associated with different features (like how far it is from a ghost or food pellet) based on the expected rewards (both immediate and cumulative) of making that move. At the end of a game, it stores these weights and uses them in the next game. Ideally it will converge on the optimal set of weights.

**How to use this project**:
Clone the repo:
`$ git clone https://github.com/pdemetci/PacMan-AI.git`
Run pacman.py:
`$ cd PacMan-AI/PacMan1`
`$ python pacman.py --pacman SimpleQPacman --agentArgs fromPickle=True`
There are many other options for pacman.py. Run `$ python pacman.py --help` for more information.
If you want the weights to initialize randomly, you can set `fromPickle=False` and see how Pacman fares.
If you want to step through the game one move at a time, you can set `--frameTime -1`, or any negative number. The default `frameTime` is 0.1, so you can make it run faster or slower.