"""
Pacman Astar

"""

from game import Agent, Directions
from numpy import ones

class SetUp(object):
	"""Setting up the grid

	Potentially use this class to initialze the position of Pacman and the 
	importnat capsules.
	"""
	def __init__(self):
		pass

class AstarPacman(Agent):
	""" Trying to get pacman to move
	state.data.food from game.Grid
	"""

	def __init__(self): 
	# 	self.coordinates = list(state.getPacmanPosition())
		self.open_list = [] #Set of nodes already evaluated
		self.closed_list = [] #Tentative nodes to be evaluated
		self.came_from = [] #map of navigated nodes

	def Astar(start, goal):
		"""Astar function that runs the show"""
		# self.g_score = 0 #cost from starting along the best known path
		# self.f_score = self.g_score + cost_estimate(start, goal)

		while len(self.open_list) > 0:
			pass




	def getAction(self, state):
		"""
		Pacman moves east
		"""
		self.coordinates = state.getPacmanPosition()
		self.capsule1_coords = state.data.capsules[0] 
		self.capsule2_coords = state.data.capsules[1]

		# coord_s = self.coordinates
		# cells_s = self.cells[coord_s]

		g_cost = 0 #Cost from starting along the best known path
		h_cost = self.get_h_cost(self.coordinates, self.capsule1_coords)
		# self.open_list = [self.coordinates]
		while len(self.open_list) > 0:
			"""Insert function that calculates the get_lowest_cost_open_coord
			- Don't need this because get_legal_coords does this
			"""
			print self.open_list
			print self.coordinates
			self.open_list = [self.coordinates]
			self.open_list.remove(self.coordinates)
			self.closed_list.append(self.coordinates)
			open_coords, costs = self.get_open_adj_coords(state, self.coordinates)
			for idx, coord in enumerate(open_coords):
				print "idx =", idx
				print "coord =", coord

				g_cost = g_cost + costs[idx]
				h_cost = self.get_h_cost(self.coordinates, self.capsule1_coords)
				f_cost = g_cost + h_cost
				if coord in self.open_list:
					old_f_cost = f_cost
					if f_cost < old_f_cost:
						parent_coords = self.coordinates
				else:
					self.open_list.append(coord)
					parents_coords = self.coordinates

		# coords = self.get_lowest_cost_open_coord()


		# print H
			# cell = 
			# g_cost = cell_s.g_cost + costs[idx]


		legal_actions = state.getLegalActions()
		# print legal_actions
		# print dir(state.data)
		# print dir(state.getPacmanPosition)
		# print state.getPacmanPosition()
		# print self.coordinates
		if "East" in legal_actions:
			return Directions.EAST
		else:
			return Directions.STOP
		# pacman_location = state.data


	def get_h_cost(self, coord_a, coord_b):
		"""Returns the h score, the manhattan distance between coord_a and the cood_b"""
		return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])


	def get_open_adj_coords(self, state, coords):
		"""returns list of valid coords that are adj. to the pacman, open 
		(and are not in the closed list(?))"""
		adj_coords = []
		directions = state.getLegalActions()
		directions.remove("Stop")
		if "West" in directions:
			W_coords = (coords[0]-1, coords[1])
			adj_coords.append(W_coords)
		if "East" in directions:
			E_coords = (coords[0]+1, coords[1])
			adj_coords.append(E_coords)
		if "North" in directions:
			N_coords = (coords[0], coords[1]+1)
			adj_coords.append(N_coords)
		if "South" in directions:
			S_coords = (coords[0], coords[1]-1)
		costs = [1]*len(adj_coords)

		
		# print directions #.remove("Stop")
		# print costs
		# print adj_coords
		return adj_coords, costs

	
	def get_lowest_cost_open_coord(self):
		pass
		# open_cells = self.open_list
		# sorted_cells = sorted(open_cells, key = lambda s: self.cells[s].f_cost)
		# costs = map(lambda c: self.cells[c].f_cost, sorted_cells)
		# return sorted_cells[0]

class path():
	"""
	For example layout, food is in [(18, 1), (1,9)]. Bottom left-hand corner = (1,1)
	"""

	def __init__(self, draw_screen, coordinates, dimensions):
		self.draw_screen = draw_screen
		self.coordinates = coordinates
		self.dimensions = dimensions
		self.color = (0,0,0)
		self.g_cost = None
		self.h_cost = None


	def f_cost(self):
	    if self.g_cost is None or self.h_cost is None:
	        return None
	    return self.g_cost + self.h_cost


	def determine_Path(self):
		""" 
		Function to optimize Pacman Path. F = G + H
		G = cost of moving from starting position to another position
		H = Number of squares left
		"""
		COST_TO_MOVE = ''
		COST_TO_MOVE = self.g_cost
		# COST_TO_MOVE = self.h_cost
		# COST_TO_MOVE = self.f_cost
		# line_width = 2
		#Want to draw a line that displays pacman path using Astar search
