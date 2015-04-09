"""
Glue for interfacing with the Berkeley code.
@author Stephanie Northway
"""

import operator
import random

import numpy as np
import pandas as pd

from game import Agent, Directions
from layout import Layout
from util import manhattanDistance

class GoWestPacman(Agent):
	"""
	Our implementation of what used to be GoWestAgent.
	Just to be sure we can do it.
	"""

	def getAction(self, state):
		"""
		Takes in a GameState object and returns a Directions.
		This will probably call our actual ML stuff.
		"""
		legal_actions = state.getLegalActions()
		if 'West' in legal_actions:
			return Directions.WEST
		else:
			return Directions.STOP

class SimpleExplorationPacman(Agent):
	"""
	A Pacman agent that uses a VERY simple q-learning algorithm in which the states
	have been encoded as "explored" and "unexplored", and Pacman can only be in one
	state (since he can't be standing in an unexplored cell). That might make it not
	actually qualify as q-learning, but you know, baby steps.
	"""
	def __init__(self):
		super(Agent, self).__init__()  # call the parent's init function
		self.Q = [0, 0]  # Q always initializes with zeros
		self.R = [1, 5]  # hard-coding R for now
		self.gamma = 0.3  # exploration parameter
		self.exploredCoords = set()  # set of coordinates Pacman has been to

	def getAction(self, state):
		"""
		Any Agent subclass must define a getAction method.

		state: the GameState object
		returns: the direction PacMan should go (e.g. Directions.NORTH)
		"""

		# add current position to exploredCoords
		self.exploredCoords.add(state.getPacmanPosition())

		rewards = self.getActionRewards(state, state.getLegalActions())

		if self.goRandomDirection():
			direction = random.choice(state.getLegalActions())
			directionReward = rewards[direction]
		else:
			direction, directionReward = max(rewards.iteritems(), key=operator.itemgetter(1))  # this currently biases toward last option, probably East
		
		self.updateQ(state, self.Q.index(directionReward), set(rewards.values()))
		
		return direction

	def getReward(self, state, action):
		"""
		Checks the Q matrix to see what we've got.

		Eventually we'll need a mapping between thes=		"""
		# if it's explored, return the "explored" Q value
		if state.generatePacmanSuccessor(action).getPacmanPosition() in self.exploredCoords:
			return self.Q[0]
		# otherwise return the "unexplored" Q value
		else:
			return self.Q[1]

	def getActionRewards(self, state, legalActions):
		"""
		Return a dictionary like {direction: reward} for all legal directions
		"""
		reward = dict.fromkeys(legalActions)
		for action in legalActions:
			reward[action] = self.getReward(state, action)
		return reward

	def updateQ(self, state, newState, legalActions):
		"""
		Update the Q matrix (brain) of our PacMan with
		Q(currentState, newState) = R(currentState, newState) + gamma * max(Q(newState, legalActions))

		state: the GameState object
		newState: 0 or 1 (explored or unexplored) -- sorry this is confusing
		legalActions: [0] or [0, 1] depending on if any unexplored cells are legally moveable-to
		"""
		self.Q[newState] = self.R[newState] + self.gamma * max(filter(lambda x: x in legalActions, self.Q))
		print self.Q



	def goRandomDirection(self):
		"""
		Should it go with the highest Q value or try something new?

		returns: boolean
		"""
		r = random.random()
		if r > self.gamma:
			return True
		else:
			return False


STATES = {
'g1_dist': 0,
'g2_dist': 0,
'c1_dist': 0, 
'c2_dist': 0,
'p_frac': 0
}

class PyBrainPacman(Agent):
	"""
	An agent based on what I just read on PyBrain's Q-learning tutorial thingy.

	It will need to have a CONTROLLER, to map states to actions;
	a LEARNER, which updates the controller parameters according to its interactions with the world;
	and an EXPLORER, which tells it when to do a less-than-optimal action.
	"""

	def __init__(self):
		super(Agent, self).__init__()  # call the parent's init function
		self.Q = pd.Series(STATES)  # Q initializes with zeros
		self.pellets_remaining = 0
		self.g1_dist = 0
		self.g2_dist = 0
		self.capsules = 0
		initialized = False
		self.explorationRate = 0.2  # exploration parameter
		# self.exploredCoords = set()  # set of coordinates Pacman has been to

	def getAction(self, state):
		"""
		I think this is the controller. Takes in a state, returns an action.
		"""
		pos = state.getPacmanPosition()

		if not initialized:
			self.pellets_remaining = state.getNumFood()
			self.g1_dist = manhattanDistance(pos, state.getGhostPosition(1))
			self.g2_dist = manhattanDistance(pos, state.getGhostPosition(2))
			self.capsules = len(state.getCapsules())

		if isExploring():
			# do some sort of softmax
			pass
		else:
			# get the best action to do next...


	def getReward(self, state):
		"""
		Function to determine the reward of the action that just happened.
		"""
		pos = state.getPacmanPosition()

		delta_food = self.pellets_remaining - state.getNumFood()
		delta_g1 = self.g1_dist - manhattanDistance(pos, state,getGhostPosition(1))
		delta_g2 = self.g2_dist - manhattanDistance(pos, state.getGhostPosition(2))
		delta_capsules = self.capsules - len(state.getCapsules())

		return 2 * delta_food + 3 * delta_g1 + 3 * delta_g2 + 6 * delta_capsules


	def updateQ(self, action, reward):
		"""
		Q(s) = Q(s) + alpha * [r + gamma * max(Q(s')) - Q(s, a)]
		"""

	def qFunction(self):
		"""
		The thing that is q
		"""
		return self.Q.g1_dist

	def isExploring(self):
		"""
		Same as goRandomDirection from other PacMan
		"""

		r = random.random()
		if r < self.explorationRate:
			return True
		else:
			return False