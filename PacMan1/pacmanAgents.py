"""
Glue for interfacing with the Berkeley code.
@author Stephanie Northway
"""

import numpy as np
from game import Agent, Directions

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
		print legal_actions
		if 'West' in legal_actions:
			return Directions.WEST
		else:
			return Directions.STOP

class ReinforcementPacman(Agent):
	def __init__(self):
		super(Agent, self).__init__()
		# How should we initialize these? When will we know the layout??
		self.Q = np.zeros([1, 1])
		self.R = np.zeros([1, 1])
		self.gamma = 1

	def getAction(self,state):
		"""
		Any Agent subclass must define a getAction method.

		state: the GameState object
		returns: the direction PacMan should go (e.g. Directions.NORTH)
		"""
		self.getReward(state)
		return Directions.STOP

	def getReward(self, state):
		# print state.getWalls().asList()
		print state.data.layout.width, state.data.layout.height
		# print state.getPacmanPosition()
		# print state.hasFood(*state.getDirection())

	def updateQ(self, state, newState):
		"""
		Update the Q matrix (brain) of our PacMan with
		Q(currentState, newState) = R(currentState, newState) + gamma * max(Q(newState, legalActions))

		state: the GameState object
		newState: 
		"""
		self.Q


class EncodedState(object):
	"""
	We might want this to be its own class?
	"""
	def __init__(self):
		pass

"""
How will we encode the states? Example: Ghost distance could be stored as the distance to the closest ghost,
either as the crow flies (rounded) or number of moves it would need to get you.
Maybe the number of states is not known in our case, and we need to add to Q? But R needs to know all of the states, soo....
Instead of being directions, what if the actions were based on velocity/current direction vectors...
- away from closest ghost
- toward closest food
- away from where it's already been

"""

