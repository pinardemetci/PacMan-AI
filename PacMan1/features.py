import random
from util import manhattanDistance
from util2 import *


class Feature(object):
    def __init__(self, value=random.random(), weight=random.random()):
        """
        Main class for all features. Each feature will inherit from this class.
        Follwing the same pattern as Agent; the index is for the
        Agent object to know which feature it is in the features list.
        """
        # Value will be used to calculate Q values.
        self.value = value  
        #Each feature has a weight associated with it which will be updated to learn which feature to prioritize.
        self.weight = weight 

    def __str__(self):
        #Tracking the values and weights of features after each update makes it easier to see how PacMan is learning 
        return "%s | value: %f | weight: %f" % (self.__class__.__name__, self.value, self.weight)

    def extractFromState(self, state, costs = None):
        """
        Map the state onto the feature space (i.e. a real number).
        Gets the value, doesn't update it.
        This will be implemented for each feature. 
        If forgot to implement, raises and error. 
        """
        raise NotImplementedError

    def updateValue(self, state, costs):
        """
        Updates the value based on the state.
        """
        self.value = self.extractFromState(state, costs)
        print self


class NearestCapsuleFeature(Feature):
    """
    Distance to the nearest capsule.
    Inherits from Feature class, like every other feature.
    Uses A-star to calculate the distance
    """

    def extractFromState(self, state, costs):
        """
        Implemented to generate the distance to the nearest capsule
        """
        pos = state.getPacmanPosition() #position of PacMan
        capsules = state.getCapsules() #state of each capsule

        # if there are capsules, return the minimum distance to a capsule
        if len(capsules) > 0:
            # caps_dists = [Astar(state, pos, c, layout) for c in capsules]
            caps_dists = [manhattanDistance(pos, c) for c in capsules]
            return min(caps_dists)
        # otherwise, return the largest distance possible in the layout so it thinks capsules are just far away.
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height)) #manhattanDistance between 2 corners in the layout.


class NearestNormalGhostFeature(Feature):
    """
    Distance to the nearest non-scared ghost.
    """

    def extractFromState(self, state, costs):
        pos = state.getPacmanPosition()
        ghosts = state.getGhostStates()
        normal_ghosts = filter(lambda g: g.scaredTimer == 0, ghosts)

        if len(normal_ghosts) > 0:
            normal_ghost_dists = [Astar(state, pos, n.getPosition(), state.data.layout, costs) for n in normal_ghosts]
            return min(normal_ghost_dists)
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))


class NearestScaredGhostFeature(Feature):
    """
    Distance to the nearest scared ghost.
    """

    def extractFromState(self, state, costs):
        pos = state.getPacmanPosition()
        ghosts = state.getGhostStates()
        scared_ghosts = filter(lambda g: g.scaredTimer > 0, ghosts)

        if len(scared_ghosts) > 0:
            scared_ghost_dists = [Astar(state, pos, s.getPosition(), state.data.layout, costs) for s in scared_ghosts]
            return min(scared_ghost_dists)
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))


class TotalFoodFeature(Feature):
    """
    Total number of food remaining on the board
    """

    def extractFromState(self, state, costs):
        return state.getNumFood()


class NearestFoodFeature(Feature):
    """
    Distance to nearest food
    """

    def extractFromState(self, state, costs):
        pos = state.getPacmanPosition()

        if state.getNumFood() > 0:
            foodDistances = [Astar(state, pos, f, state.data.layout, costs) for f in state.getFood().asList()]
            return min(foodDistances)
        else:
            return 0
