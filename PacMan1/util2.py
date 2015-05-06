"""
@authors: Kelly Brennan, Stephanie Norway and Pinar Demetci
Our own utility functions and classes.
"""


class Tile(object):
    """
    Represents a position on the board in terms of what it will cost Pacman to get there.
    For example layout, food is in [(18, 1), (1,9)]. Bottom left-hand corner = (1,1).

    coordinates: the coordinates of this tile
    g_cost: total cost of moving the agent from a start position to a given square
    h_cost: number of total moves (as the crow flies) to goal
    f_cost: the score for this Tile
    """
    def __init__(self, coordinates, g_cost=None, h_cost=None, f_cost=None):
        self.coordinates = coordinates
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = f_cost

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return str(self.coordinates)


def initializeTiles(layout):
    """
    Initializes the open positions on the board as Tile objects. This
    gets called once at the beginning of a game.

    layout: the Layout object for the game
    returns: a dictionary like {(x, y): Tile((x, y))}
    """
    costs = {}  # Dictionary the size of the game board to g, h, and f cost values
    for x in range(layout.width):
        for y in range(layout.height):
            costs[(x, y)] = Tile((x, y))
    return costs


def DepthFirstSearch(state, start, costs, closed_list=[]):
    """
    Depth-first search algorithm to find close food pellets with greater computational efficiency than running
    Astar on every position with food.
    Recursive function, until it finds a food pellet
    First, finds a list of open adjacent coordinates. If food at coordinate, return distance from Pacman
        Otherwise, run function with new coordinate input

    Failure mode: function doesn't work when pacman eats a food pellet. 
    Next steps would be to address this.

    state: the GameState object
    start: (x, y) coordinates from which to start the search
    costs: {(x, y): Tile((x, y))}
    closed_list: list of coordinates no longer being considered
    returns: Astar distance to the closest food pellet
    """
    if start not in closed_list:
        closed_list.append(start)  # start position is off limits
    open_coords = get_open_adj_coords_DFS(state, start, state.data.layout)
    for coord in open_coords:
        if state.hasFood(*coord):
            astar_distance = Astar(state, start, coord, state.data.layout, costs)
            return astar_distance
        elif coord not in closed_list:
            DepthFirstSearch(state, coord, costs, closed_list)
        else:
            pass


def Astar(state, start, goal, layout, costs):
    """Astar function that runs the show
    Determines the distance between a position and a goal with obstacles, such as walls present

    start: initial position of search (tuple)
    goal: end position of search (tuple)
    layout: Layout object for game
    costs: dictionary of tile objects that can be accessed with coordinate keys
    returns: distance between start and goal
    """
    goal_int = (int(goal[0]), int(goal[1])) #convert goal position from a float to an integer for algorithm not to enter an infinite loop
    open_list = []  # Set of nodes already evaluated
    costs[start].g_cost = 0
    costs[start].h_cost = get_h_cost(start, goal_int)
    costs[start].f_cost = costs[start].g_cost + costs[start].h_cost
    open_list.append(costs[start])

    while len(open_list) > 0:
        tile = get_lowest_cost_open_coord(open_list)
        open_list.remove(tile)
        open_coords, tile_cost = get_open_adj_coords(state, tile.coordinates, layout)
        for i, coord in enumerate(open_coords):
            if coord == goal_int:
                costs[coord].g_cost = tile.g_cost + tile_cost[i]
                costs[coord].h_cost = get_h_cost(coord, goal_int)
                costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost
                return costs[coord].f_cost

            elif costs[coord] not in open_list:
                open_list.append(costs[coord])
                costs[coord].g_cost = tile.g_cost + tile_cost[i]
                costs[coord].h_cost = get_h_cost(coord, goal_int)
                costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost
            else:
                if costs[coord].f_cost > costs[coord].g_cost + costs[coord].h_cost:
                    costs[coord].f_cost = costs[coord].g_cost + costs[coord].h_cost


def get_h_cost(coord_a, coord_b):
    """
    Calculate h_cost of given position and goal

    coord_a: starting coordinate
    coord_b: goal coordinate
    Returns: the h score, the manhattan distance between coord_a and the cood_b
    """
    return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])


def get_open_adj_coords(state, coords, layout):
    """
    Finds the coordinates of the up to four open adjacent positions to coords.

    coords: the center coordinate pair
    layout: the Layout object for the game
    returns: (list of open adjacent coordinates, ones(same length))
    """
    adj_coords = []
    if not layout.isWall((coords[0] - 1, coords[1])):
        adj_coords.append((coords[0] - 1, coords[1]))
    if not layout.isWall((coords[0] + 1, coords[1])):
        adj_coords.append((coords[0] + 1, coords[1]))
    if not layout.isWall((coords[0], coords[1] + 1)):
        adj_coords.append((coords[0], coords[1] + 1))
    if not layout.isWall((coords[0], coords[1] - 1)):
        adj_coords.append((coords[0], coords[1] - 1))
    else:
        pass
    costs = [1] * len(adj_coords)
    return adj_coords, costs


def get_open_adj_coords_DFS(state, coords, layout):
    """
    Get open adjacent coordinates for the DepthFirstSearch function.

    coords: the center coordinate pair
    layout: the Layout object for the game
    returns: list of open adjacent coordinate pairs
    """
    adj_coords = []
    if not layout.isWall((coords[0] - 1, coords[1])):
        adj_coords.append((coords[0] - 1, coords[1]))
    if not layout.isWall((coords[0] + 1, coords[1])):
        adj_coords.append((coords[0] + 1, coords[1]))
    if not layout.isWall((coords[0], coords[1] + 1)):
        adj_coords.append((coords[0], coords[1] + 1))
    if not layout.isWall((coords[0], coords[1] - 1)):
        adj_coords.append((coords[0], coords[1] - 1))
    else:
        pass
    return adj_coords


def get_lowest_cost_open_coord(open_list):
    """
    Find the tile with the lowest cost.

    open_list: list of Tile objects to sort
    returns: open_list sorted by f_cost
    """
    return sorted(open_list, key = lambda t: t.f_cost)[0]
