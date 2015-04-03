"""
1) Getting and storing data from different maps. To be used for Q-learning matrix
"""

from game import Agent, Directions
from numpy import zeros
import random

class RMatrix(Agent):
	"""
	1) Receiving Map Data
	"""
	def getAction(self, state):
		legal_actions = state.getLegalActions()
		R_matrix = ([-1, 0, -1, -1, -1, -1, -1, -1], [0, -1, 0, -1, -1, -1, -1, -1], 
			[-1, 0, -1, 0, -1, -1, -1, -1], [-1, -1, 0, -1, 0, -1, -1, -1], 
			[-1, -1, -1, 0, -1, 0, -1, -1], [-1, -1, -1, -1, 0, -1, 0, -1], 
			[-1, -1, -1, -1, -1, 0, -1, 100], [-1, -1, -1, -1, -1, -1, 0, 100])
		Q_matrix = zeros(shape = (8,8))
		legal_actions.remove('Stop')
		print legal_actions
		print state.getPacmanState()
		print state.getPacmanPosition()
		move_dir = random.choice(legal_actions)
		if move_dir == "East":
			return Directions.EAST
		if move_dir == "West":
			return Directions.WEST

		# print state.data
		# if "West" in legal_actions:
		# 	# print state.data
		# 	# print state.data.agentStates
		# 	return Directions.WEST
		# else:
		# 	# print state.data
		# 	# print state.data.agentStates
		# 	return Directions.STOP
		# print state.data
		# print state.data.agentStates

	def Q_learningFunction(self, Rmatrix, Qmatrix):
		"""Q-learning Function that does computation"""
		gamma = 0.5
		Q = R + Gamma*Max[Q]
		pass


	def selectAction(self, state):
		""" Randomly choose an action
		input: list of actions
		output: possible next action
		"""
		pass

class Qmatrix(Agent):
	Q_matrix = zeros(shape = (8,8))

def print_Matrix(matrix):
	for line in matrix:
		print line
