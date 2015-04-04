"""
Simple implementation of Q-learning on testMaze layout.

run in T using: python pacman.py --layout testMaze --pacman QLearning

Helped us better understand implementation in pacman program
based on: http://mnemstudio.org/path-finding-q-learning-tutorial.htm
"""

from game import Agent, Directions
from numpy import zeros, matrix
import random
from os.path import exists

class QLearning(Agent):
	"""
	Basic Pacman example doing Q-Learning
	"""
	def getAction(self, state):
		legal_actions = state.getLegalActions()
		legal_actions.remove('Stop')
		R_matrix = matrix([[-1, 0, -1, -1, -1, -1, -1, -1], [0, -1, 0, -1, -1, -1, -1, -1], 
			[-1, 0, -1, 0, -1, -1, -1, -1], [-1, -1, 0, -1, 0, -1, -1, -1], 
			[-1, -1, -1, 0, -1, 0, -1, -1], [-1, -1, -1, -1, 0, -1, 0, -1],
			[-1, -1, -1, -1, -1, 0, -1, 100], [-1, -1, -1, -1, -1, -1, 0, 100]])
		Q_matrix = zeros(shape = (8,8))
		state = 8 - state.getPacmanPosition()[0] #8 total states. Initialize
		print "Pacman state", state
		move_dir = self.Q_learningFunction(R_matrix, Q_matrix, state)
		print Q_matrix
		if move_dir == "E" and "East" in legal_actions:
			return Directions.EAST
		if move_dir == "W" and "West" in legal_actions:
			return Directions.WEST


	def Q_learningFunction(self, R, Q, state):
		"""
		Q-learning Function that does computation

		input: R_matrix, Q_matrix, pacman state
		output: pacman direction based on algorithm
		"""
		gamma = 0.5 
		best_action, action = self.choose_action(state, [R[state, state], R[state,state+1], R[state, state-1]])
		Q[state,action] = R[state, action] + gamma*best_action
		if state > action:
			return 'E'
		elif state < action:
			return 'W'


	def choose_action(self, state, values):
		"""
		choose a direciton based on the R maxtrix value
		selects action based on rewards encoded in R matrix
		"""
		choose_action = max(values)
		i = values.index(max(values))
		if i == 0 or i == 1:
			index = state + i
		elif i == 2:
			index = state - 1
		return choose_action, index


	def store_Q(self, Q):
		"""Store Q maxtrix"""
		pass