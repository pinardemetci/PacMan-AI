"""
Simple implementation of Q-learning on testMaze layout.

run in T using: python pacman.py --layout testMaze --pacman QLearning

Helped us better understand implementation in pacman program
based on: http://mnemstudio.org/path-finding-q-learning-tutorial.htm
"""

from game import Agent, Directions, GameStateData, Game
# from pacman import Game
from numpy import zeros, matrix, array
from joblib import dump, load
import random
from os.path import exists
import pickle
# from pickle import dump, load
import time
import csv

class QLearning(Agent):
	"""
	Basic Pacman example doing Q-Learning
	"""
	def __init__(self):
		self.R_matrix = matrix([[-1, 0, -1, -1, -1, -1, -1, -1], [0, -1, 0, -1, -1, -1, -1, -1], 
			[-1, 0, -1, 0, -1, -1, -1, -1], [-1, -1, 0, -1, 0, -1, -1, -1], 
			[-1, -1, -1, 0, -1, 0, -1, -1], [-1, -1, -1, -1, 0, -1, 0, -1],
			[-1, -1, -1, -1, -1, 0, -1, 100], [-1, -1, -1, -1, -1, -1, 0, 100]])
		# self.Q_matrix = zeros(shape = (8,8))
		self.Q_matrix = self.return_Q() #zeros(shape = (8,8))#self.return_Q()
		self.gamma = 0.5 
		self.counter = pickle.load(open("counter.p", 'rb'))


	def getAction(self, state):
		legal_actions = state.getLegalActions()
		# print legal_actions
		legal_actions.remove('Stop')
		Pacstate = 8 - state.getPacmanPosition()[0] #8 total states. Initialize 
		print "Pacman state", Pacstate
		move_dir = self.Q_learningFunction(self.R_matrix, self.Q_matrix, Pacstate)
		""" Updates Q Matrix with every pacman movement"""
		# if Pacstate == 0:
		# 	self.store_Q(self.Q_matrix)
		# else:
		# 	self.store_Q(self.Q_matrix, False)

		""" Updates Q matrix at end of pacman game (Hard code)"""
		if Pacstate == 6:
			self.store_Q(self.Q_matrix, self.counter)

		if state.isWin() == True:
			print "I win"

		if move_dir == "E" and "East" in legal_actions:
			return Directions.EAST
		elif move_dir == "W" and "West" in legal_actions:
			return Directions.WEST


	def Q_learningFunction(self, R, Q, state):
		"""
		Q-learning Function that does computation

		input: R_matrix, Q_matrix, pacman state
		output: pacman direction based on algorithm
		"""
		best_action, action = self.choose_action(state, [R[state, state], R[state,state+1], R[state, state-1]])
		print best_action, action
		Q[state,action] = R[state, action] + self.gamma*best_action
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


	def store_Q(self, Q, counter, reset = False):
		"""Store Q matrix
		input: Q matrix to be stored, counter
		output: pickling files with data
		"""
		Q_file = "Q_matrix.p"
		print Q
		if counter == 0 or reset:
			counter = 1
			dump(Q, Q_file)
			pickle.dump(counter, open("counter.p", 'wb'))
		else: 
			pickle.dump(counter + 1, open("counter.p", "wb"))
			dump(Q, Q_file)


	def return_Q(self):
		""" Retrieves the Q matrix stored in Q_matrix.p
		output = Q_matrix
		"""
		Q_new = load("Q_matrix.p")
		return Q_new