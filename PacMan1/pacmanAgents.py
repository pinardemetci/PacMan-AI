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
		self.Q = None
		self.R = None

	def getAction(self,state):
		"""
		Any Agent subclass must define a getAction method.

		state: the GameState object
		returns: the direction PacMan should go (e.g. Directions.NORTH)
		"""
		self.getReward(state)
		return Directions.WEST

	def getReward(self,state):
		print state.getPacmanPosition()
		print state.hasFood(*state.getPacmanPosition())

	def updateQ(self, gamma=0.8):
		pass

