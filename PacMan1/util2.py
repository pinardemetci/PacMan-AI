"""
Pacman Astar

Our own util function to implement the features with Astar instead of MahattanDistance
"""

from game import *
from pacman import *
import layout
from numpy import ones
import copy
import util

def Astar(state, start, goal, layout):
	"""Astar function that runs the show"""
	open_list = [] #Set of nodes already evaluated
	costs = {} #The size of the game board to store g, h and f cost values
	# print layout.width
	# print layout.height
	for x in range(layout.width):
		#print x
		for y in range(layout.height):
			costs[(x, y)] = Tile((x,y))
	# print layout.width
	# print layout.height
	#print costs
	#print state.getPacmanState()
	costs[start].g_cost = 0
	costs[start].h_cost = get_h_cost(start, goal)
	costs[start].f_cost = costs[start].g_cost + costs[start].h_cost
	open_list.append(costs[start])
	# print "open_list", open_list


	while len(open_list) > 0:
		# print open_list
		tile = get_lowest_cost_open_coord(open_list)
		open_list.remove(tile)
		# closed_list.append(tile)
		open_coords, tile_cost = get_open_adj_coords(state, tile.coordinates, layout)
		# print open_coords, tile_cost
		for i, coord in enumerate(open_coords):
			if coord == goal:
				costs[coord].g_cost = tile.g_cost + tile_cost[i]
				costs[coord].h_cost = get_h_cost(coord, goal)
				costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost
			# elif layout.isWall(coord) == True:
			# 	costs[coord].f_cost = 300.0
				# print costs[coord].g_cost
				# print costs[coord].h_cost

				# print "Coord, cost", costs[coord], costs[coord].f_cost
				return costs[coord].f_cost

			elif costs[coord] not in open_list:
				open_list.append(costs[coord])
				costs[coord].g_cost = tile.g_cost + tile_cost[i]
				costs[coord].h_cost = get_h_cost(coord, goal)
				costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost
				# return 300
			else:
				if costs[coord].f_cost > costs[coord].g_cost + costs[coord].h_cost:
					costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost
				return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))
	#print open_list
def get_h_cost(coord_a, coord_b):
	"""Returns the h score, the manhattan distance between coord_a and the cood_b"""
	return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])


def get_open_adj_coords(state, coords, layout):
	"""returns list of valid coords that are adj. to the pacman, open 
	(and are not in the closed list(?))"""
	adj_coords = []
	# configuration_copy = copy.deepcopy(state.getPacmanState().configuration)
	# configuration_copy.pos = coords
	# print dir(state)s
	#print state.__class__.__name__
	#directions = state.getLegalActions_Tile(configuration_copy, state)
	walls = layout.isWall(coords)
	directions = state.getLegalActions()
	#print directions
	# directions.remove("Stop")
	if not layout.isWall((coords[0]-1, coords[1])):
		adj_coords.append((coords[0]-1, coords[1]))
	if not layout.isWall((coords[0]+1, coords[1])):
		adj_coords.append((coords[0]+1, coords[1]))
	if not layout.isWall((coords[0], coords[1]+1)):
		adj_coords.append((coords[0], coords[1]+1))
	if not layout.isWall((coords[0], coords[1]-1)):
		adj_coords.append((coords[0], coords[1]-1))
	else: pass
	#print "current coord:", coords
	#print adj_coords
	costs = [1]*len(adj_coords)
	return adj_coords, costs
	
def get_lowest_cost_open_coord(open_list):
	"""Return the tile with the lowest cost"""
	return sorted(open_list, key = lambda t: t.f_cost)[0]

class Tile():
	"""
	For example layout, food is in [(18, 1), (1,9)]. Bottom left-hand corner = (1,1)
	"""
	def __init__(self, coordinates, g_cost = None, h_cost = None, f_cost = None):
		self.coordinates = coordinates
		self.g_cost = g_cost
		self.h_cost = h_cost
		self.f_cost = f_cost

	def __str__(self):
		return str(self.coordinates)

	def __repr__(self):
		return str(self.coordinates)
