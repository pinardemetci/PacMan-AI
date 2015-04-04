"""
Glue for interfacing with the Berkeley code.
@author Stephanie Northway
"""

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
		print legal_actions
		if 'West' in legal_actions:
			return Directions.WEST
		else:
			return Directions.STOP

class ReinforcementPacman(Agent):
	def __init__(self):
		super(Agent, self).__init__()
		# How should we initialize these? When will we know the layout??
		self.Q = None
		self.R = None
		self.gamma = 1
	def getAction(self,state):
		"""
		Any Agent subclass must define a getAction method.

		state: the GameState object
		returns: the direction PacMan should go (e.g. Directions.NORTH)
		"""
		self.getReward(state)
		return Directions.STOP

	def initializeMatrices(self):
		#states = self.data.layout.
		self.Q = np.zeros([widthheight])

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


"""
How will we encode the states? Example: Ghost distance could be stored as the distance to the closest ghost,
either as the crow flies (rounded) or number of moves it would need to get you.
Maybe the number of states is not known in our case, and we need to add to Q? But R needs to know all of the states, soo....
Instead of being directions, what if the actions were based on velocity/current direction vectors...
- away from closest ghost
- toward closest food
- away from where it's already been

"""

