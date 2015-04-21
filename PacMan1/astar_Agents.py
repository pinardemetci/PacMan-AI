"""
Pacman Astar
<<<<<<< HEAD

"""

from game import Agent, Directions

class MovePacman(Agent):
	""" Trying to get pacman to move
	state.data.food from game.Grid

	"""

=======
"""
from game import Agent, Directions
class MovePacman(Agent):
	""" Trying to get pacman to move
	state.data.food from game.Grid
	"""
>>>>>>> master
	def getAction(self, state):
		"""
		Pacman moves east
		"""
		legal_actions = state.getLegalActions()
		# print legal_actions
		if "East" in legal_actions:
			print state.data.capsules
<<<<<<< HEAD
			print dir(state)
=======
			# print dir(state)
>>>>>>> master
			return Directions.EAST
		else:
			print state.data.capsules
			return Directions.STOP
<<<<<<< HEAD
		# pacman_location = 

	

=======
			# pacman_location =
>>>>>>> master
class path():
	"""
	For example layout, food is in [(18, 1), (1,9)]. Bottom left-hand corner = (1,1)
	"""
<<<<<<< HEAD

=======
>>>>>>> master
	def __init__(self, draw_screen, coordinates, dimensions):
		self.draw_screen = draw_screen
		self.coordinates = coordinates
		self.dimensions = dimensions
		self.color = (0,0,0)
		self.g_cost = None
		self.h_cost = None
<<<<<<< HEAD

	def f_cost(self):
		""" 
=======
	def f_cost(self):
		"""
>>>>>>> master
		Function to optimize Pacman Path. F = G + H
		G = cost of moving from starting position to another position
		H = Number of squares left
		"""
		COST_TO_MOVE = ''
		COST_TO_MOVE = self.g_cost
		# COST_TO_MOVE = self.h_cost
		# COST_TO_MOVE = self.f_cost
		line_width = 2
<<<<<<< HEAD
		#Want to draw a line that displays pacman path using Astar search
=======
		#Want to draw a line that displays pacman path using Astar search
>>>>>>> master
