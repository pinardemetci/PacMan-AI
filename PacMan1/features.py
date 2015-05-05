import random
from util import manhattanDistance
from util2 import Astar



class Feature(object):
    def __init__(self, value=random.random(), weight=random.random()):
        """
        Main class for all features. Each feature will inherit from this class.
        Follwing the same pattern as Agent; the index is for the
        Agent object to know which feature it is in the features list.

        Value: attribute to calculate Q-values
        weight: each feature has a weight associated with it, which will be updated for agent to learn
            which feature to prioritize
        """
        self.value = value  
        self.weight = weight 

    def __str__(self):
        """
        Allows the tracking the values and weights of features after each update 
        makes it easier to see how PacMan is learning 
        """
        return "%s | value: %f | weight: %f" % (self.__class__.__name__, self.value, self.weight)

    def extractFromState(self, state, costs = None):
        """
        Map the state onto the feature space (i.e. a real number).
        Gets the value, doesn't update it.
        This will be implemented for each feature. 
        If forgot to implement, raises and error. 

        state: GameState object, 
        costs: tile objects of game layout - only necessary for some features
        """
        raise NotImplementedError

    def updateValue(self, state, costs):
        """
        Updates the value based on the state.

        state: GameState object
        costs: tile objects of game layout
        """
        self.value = self.extractFromState(state, costs)


class NearestCapsuleFeature(Feature):
    """
    Distance to the nearest capsule.
    Inherits from Feature class, like every other feature.
    Uses A-star to calculate the distance
    """

    def extractFromState(self, state, costs):
        """
        Implemented to generate the distance to the nearest capsule

        state: GameState object
        costs: tile object of game layout
        """
        pos = state.getPacmanPosition() #position of PacMan
        capsules = state.getCapsules() #state of each capsule

        # if there are capsules, return the minimum distance to a capsule
        if len(capsules) > 0:
            caps_dists = [Astar(state, pos, c, state.data.layout, costs) for c in capsules]
            return min(caps_dists)
        # otherwise, return the largest distance possible in the layout so it thinks capsules are just far away.
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height)) #manhattanDistance between 2 corners in the layout.


class NearestNormalGhostFeature(Feature):
    """
    Distance to the nearest non-scared (normal) ghost.
    Implements Astar search algorithm
    """

    def extractFromState(self, state, costs):
        """
        determine distance between pacman and a normal ghost

        state: GameState object
        costs: tile object of game layout
        """
        pos = state.getPacmanPosition()
        ghosts = state.getGhostStates() 
        normal_ghosts = filter(lambda g: g.scaredTimer == 0, ghosts) 

        if len(normal_ghosts) > 0:
            normal_ghost_dists = [Astar(state, pos, n.getPosition(), state.data.layout, costs) for n in normal_ghosts]
            return min(normal_ghost_dists)
            #if there are no ghosts:
        else:
            #return the largest distance possible
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))


class NearestScaredGhostFeature(Feature):
    """
    Distance to the nearest scared ghost after PacMan eats a capsule.
    Implements Astar search algorithm
    """

    def extractFromState(self, state, costs):
        """
        determine distance between pacman and a scared ghost

        state: GameState object
        costs: tile object of game layout
        """
        pos = state.getPacmanPosition()
        ghosts = state.getGhostStates() #state of all the ghosts.
        scared_ghosts = filter(lambda g: g.scaredTimer > 0, ghosts) #filters the ones that are in scared time.

        #After PacMan eats a capsule, scared time starts.
        #When there are scared ghosts, return A-star distance to the nearest one
        if len(scared_ghosts) > 0:
            scared_ghost_dists = [Astar(state, pos, s.getPosition(), state.data.layout, costs) for s in scared_ghosts]
            return min(scared_ghost_dists)
        #If none exists, return the largest distance possible, making PacMan think they are just really far. 
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))


class TotalFoodFeature(Feature):
    """
    Feature Total number of food remaining on the board.
    This feature exists so that PacMan will care about eating all the food.
    """

    def extractFromState(self, state, costs):
        """
        Returns the total number of food.

        state: GameState object
        costs: tile object of game layout - not used here
        """
        return state.getNumFood()


class NearestFoodFeature(Feature):
    """
    Distance to nearest food
    Inherits from Feature
    """

    def extractFromState(self, state, costs):
        """
        Uses manhattanDistance instead of A-star to speed up the process.

        state: GameState object
        costs: tile object of game layout - not used here
        """
        pos = state.getPacmanPosition()
        #if food exists:
        if state.getNumFood() > 0:
            #return the manhattanDistance to the nearest food
            foodDistances = [manhattanDistance(pos, f) for f in state.getFood().asList()]
            return min(foodDistances)
        #if all food is consumed
        else:
            #it actually means game is won, return 0.
            return 0


class ScoreFeature(Feature):
    """
    game score
    """
    def extractFromState(self, state, costs):
        """
        Calculate the game score

        state: GameState object
        costs: tile object of game layout - not used here
        """
        return state.getScore()*0.01 #multiply constant to manage weight values from becoming exceedingly large
