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
from actions import AstarAction, RunawayAction

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
class SimpleQPacman(Agent):
	"""
	Starting over, AGAIN, after meeting with Paul.
	"""
	def __init__(self):
		super(Agent, self).__init__()
		# FEATURE_NAMES = ['mean_food_dist', 'nearest_capsule_dist', 'nearest_ghost_dist']
		FEATURE_NAMES = ['mean_food_dist']
		# making this a dict will let us refer to features by names
		# self.features = dict(zip(FEATURE_NAMES, np.zeros(len(FEATURE_NAMES))))
		self.features = [0, 0]
		self.weights = [-1, -2]
		self.b = 0.5
		self.explorationRate = 0.6
		self.reward = 0
	def getAction(self, state):
		"""
		Takes in a GameState object, calculates the optimal (or not)
		next action, returns that action.
		"""
		self.updateWeights(state)
		legalActions = state.getLegalActions()
		legalActions.remove(Directions.STOP)
		print legalActions
		q = dict(zip(legalActions, np.zeros(len(legalActions))))
		action = Directions.STOP
		for i in range(len(self.features)):
			for a in legalActions:
				newstate = state.generateSuccessor(0, a)
				q[a] += self.extractFeaturesFromState(newstate)[i] * self.weights[i] + self.b
			print q
			q_max = max(q.values())
		for k, v in q.items():
			if v == q_max:
				print k
				action = k
			if self.isExploring():
				final_action = random.choice(legalActions)
			else:
				final_action = action
				# state.generatePacmanSuccessor(action).getPacmanPosition() in self.exploredCoords:
				next_pos = state.generateSuccessor(0, final_action).getPacmanPosition()
				self.reward = int(state.hasFood(*next_pos))
			return final_action
	def updateWeights(self, state):
		"""
		Change weights of each feature based on the change in that
		feature from the last state.
		If the last action
		"""
		prevFeatures = np.asarray(self.features)
		newFeatures = np.asarray(self.extractFeaturesFromState(state))
		delta_features = newFeatures - prevFeatures
		# mean food distance
		self.weights[0] -= delta_features[0] * self.reward
		# capsule distance
		self.weights[1] -= delta_features[1] * self.reward
		# update self.features
		self.features = self.extractFeaturesFromState(state)
	def extractFeaturesFromState(self, state):
		pos = state.getPacmanPosition()
		food = state.getFood().asList()
		if len(food) > 0:
			mean_food_dist = np.average([manhattanDistance(pos, f) for f in food])
			self.features[0] = mean_food_dist
		else:
			self.features[0] = 0
			capsules = state.getCapsules()
		if len(capsules) > 0:
			caps_dists = [manhattanDistance(pos, c) for c in capsules]
			self.features[1] = min(caps_dists)
		else:
			self.features[1] = 0
		return self.features
		# ghosts = state.getGhostPositions()
		# ghost_dists = [manhattanDistance(pos, g) for g in ghosts]
		# self.features['nearest_ghost_dist'] = min(ghost_dists)
	def isExploring(self):
		"""
		Stolen from my other agent classes
		"""
		r = random.random()
		if r < self.explorationRate:
			return True
		else:
			return False
class SimpleExplorationPacman(Agent):
	"""
	A Pacman agent that uses a VERY simple q-learning algorithm in which the states
	have been encoded as "explored" and "unexplored", and Pacman can only be in one
	state (since he can't be standing in an unexplored cell). That might make it not
	actually qualify as q-learning, but you know, baby steps.
	"""
	def __init__(self):
		super(Agent, self).__init__() # call the parent's init function
		self.Q = [0, 0] # Q always initializes with zeros
		self.R = [1, 5] # hard-coding R for now
		self.gamma = 0.3 # exploration parameter
		self.exploredCoords = set() # set of coordinates Pacman has been to
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
			direction, directionReward = max(rewards.iteritems(), key=operator.itemgetter(1)) # this currently biases toward last option, probably East
			self.updateQ(state, self.Q.index(directionReward), set(rewards.values()))
		return direction
	def getReward(self, state, action):
		"""
		Checks the Q matrix to see what we've got.
		Eventually we'll need a mapping between thes= """
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
	# class ActualReinforcementPacman(Agent):
	# """
	# An agent based on what I just read on PyBrain's Q-learning tutorial thingy.
	# It will need to have a CONTROLLER, to map states to actions;
	# a LEARNER, which updates the controller parameters according to its interactions with the world;
	# and an EXPLORER, which tells it when to choose a less-than-optimal action in the name of adventure.
	# """
	# STATE_VARS = [
	# 'g1_dist', # manhattan distance from first ghost
	# 'g2_dist', # manhattan distance from second ghost
	# 'c1_dist', # manhattan distance from first capsule (do these states get deleted once capsules are gone?)
	# 'c2_dist', # manhattan distance from second capsule (ditto) -- maybe set to inf and map reward to zero for inf?
	# 'ex_bool' # represents whether the current cell has been previously explored
	# ]
	# ACTIONS = [AstarAction, RunawayAction]
	# STATES =
	# def __init__(self):
	# super(Agent, self).__init__() # call the parent's init function
	# self.initialized = False # we need some information that we don't have upon instantiation
	# self.R = np.zeros(len(ACTIONS), len(STATES))
	# self.actions = ACTIONS
	# self.pellets_remaining = 0
	# self.g1_dist = 0
	# self.g2_dist = 0
	# self.capsules = 0
	# self.explorationRate = 0.2 # exploration parameter
	# self.exploredCoords = set() # set of coordinates Pacman has been to
	# def computeStates(self, layout):
	# """
	# Uses the layout to compute the number of states based on max manhattan distances
	# """
	# # (0, 0) and the actual furthest corner are both walls
	# furthest_corner = (layout.width - 1, layout.height - 1)
	# max_manhattan_distance = ((1, 1), furthest_corner)
	# r = range(0, max_manhattan_distance)
	# # should also make a function for breaking up the board into arbitrary chunks
	# def getAction(self, state):
	# """
	# I think this is the controller. Takes in a state, returns an action.
	# """
	# pos = state.getPacmanPosition()
	# if not initialized:
	# self.pellets_remaining = state.getNumFood()
	# self.g1_dist = manhattanDistance(pos, state.getGhostPosition(1))
	# self.g2_dist = manhattanDistance(pos, state.getGhostPosition(2))
	# self.capsules = len(state.getCapsules())
	# self.initialized = True
	# return Directions.STOP
	# if isExploring():
	# # do some sort of softmax
	# pass
	# else:
	# # get the best action to do next...
	# self.getOptimalAction()
	# def getReward(self, state):
	# """
	# """
	# pass
	# # def getReward(self, state):
	# # """
	# # Function to determine the reward of the action that just happened.
	# # """
	# # pos = state.getPacmanPosition()
	# # delta_food = self.pellets_remaining - state.getNumFood()
	# # delta_g1 = self.g1_dist - manhattanDistance(pos, state,getGhostPosition(1))
	# # delta_g2 = self.g2_dist - manhattanDistance(pos, state.getGhostPosition(2))
	# # delta_capsules = self.capsules - len(state.getCapsules())
	# # return 2 * delta_food + 3 * delta_g1 + 3 * delta_g2 + 6 * delta_capsules
	# def getOptimalAction(self):
	# """
	# Look at Q and figure out what to do next
	# """
	# # run generatesuccessor (a heavily modified version that returns a state?)
	# # for the state it generates, get the max q value among the actions
	# # (I assume all actions are going to be legal, so that's nice)
	# pass
	# def updateQ(self, action, reward):
	# """
	# Q(s,a) = Q(s,a) + alpha * [r + gamma * max(Q(s', a')) - Q(s, a)]
	# """
	# pass
