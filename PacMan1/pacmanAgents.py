"""
Glue for interfacing with the Berkeley code.
@author Stephanie Northway
"""

import operator
import random

import numpy as np

from game import Agent, Directions
from layout import Layout

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
<<<<<<< HEAD
		super(Agent, self).__init__()  # call the parent's init function
		self.Q = [0, 0]  # Q always initializes with zeros
		self.R = [1, 5]  # hard-coding R for now
		self.gamma = 0.3  # exploration parameter
		self.exploredCoords = set()  # set of coordinates Pacman has been to

	def getAction(self, state):
=======
		super(Agent, self).__init__()
		# How should we initialize these? When will we know the layout??
		self.Q = None
		self.R = None
		self.gamma = 1
	def getAction(self,state):
>>>>>>> 314770c2d3ca728e7e90661688b904c36cdb8cb3
		"""
		Any Agent subclass must define a getAction method.

		state: the GameState object
		returns: the direction PacMan should go (e.g. Directions.NORTH)
		"""

<<<<<<< HEAD
		# add current position to exploredCoords
		self.exploredCoords.add(state.getPacmanPosition())

		rewards = self.getActionRewards(state, state.getLegalActions())
=======
	def initializeMatrices(self):
		#states = self.data.layout.
		self.Q = np.zeros([widthheight])
>>>>>>> 314770c2d3ca728e7e90661688b904c36cdb8cb3

		if self.goRandomDirection():
			direction = random.choice(state.getLegalActions())
			directionReward = rewards[direction]
		else:
			direction, directionReward = max(rewards.iteritems(), key=operator.itemgetter(1))  # this currently biases toward last option, probably East
		
		self.updateQ(state, self.Q.index(directionReward), set(rewards.values()))
		
		return direction

	def getReward(self, state, action):
		"""
		Checks the Q matrix to see what we've got
		"""
		if state.generatePacmanSuccessor(action).getPacmanPosition() in self.exploredCoords:
			return self.Q[0]
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
<<<<<<< HEAD
		self.Q[newState] = self.R[newState] + self.gamma * max(filter(lambda x: x in legalActions, self.Q))
		print self.Q

=======
		self.Q

					
class Node(object):
	def __init__(self, position):
		self.position = position
	def isExplored(self):
		pass

class Edge(object):
	def __init__(self, (Node1,Node2)):
		self.Nodes=(Node1,Node2)
	def isExplored(self):
		pass

class EncodedState(object):

	"""
	We might want this to be its own class?
	"""
	def __init__(self, layout):
		for l in layout.getList():
			if layout.isWall(l):
				pass
			else:
				x,y = l
				adjCoordinates=[]
				adjCoordinates.append(layout.isWall((x+1,y)))
				adjCoordinates.append(layout.isWall((x-1,y)))
				adjCoordinates.append(layout.isWall((x,y+1)))
				adjCoordinates.append(layout.isWall((x,y-1)))
				count= adjCoordinates.count(True)
				if count<=1:
					enc_state[Node((x,y))]=[]

		nodePositions=[]

		for node in enc_state:
			pos=node.position
			nodePositions.append(pos)
			#positive x axis
			for i in range(100):
				if (x+i,y) in nodePositions:
					a=Edge((node, Node((x+i,y))))
					enc_state[node].append(a)
					break
				else: pass
			#negative x axis
			for i in range(100):
				if (x-i,y) in nodePositions:
					a=Edge((node, Node((x+i,y))))
					enc_state[node].append(a)
					break
				else: pass
			#positive y axis
			for i in range(100):
				if (x,y+i) in nodePositions:
					a=Edge((node, Node((x,y+i))))
					enc_state[node].append(a)
					break
				else: pass
			#negative y axis
			for i in range(100):
				if (x,y-i) in nodePositions:
					a=Edge((node, Node((x,y-i))))
					enc_state[node].append(a)
					break
				else: pass

>>>>>>> 314770c2d3ca728e7e90661688b904c36cdb8cb3

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
