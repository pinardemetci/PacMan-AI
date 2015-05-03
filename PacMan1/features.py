import random
from util import manhattanDistance
from util2 import *


class Feature(object):
    def __init__(self, value=random.random(), weight=random.random()):
        """
        Follwing the same pattern as Agent; the index is for the
        Agent object to know which one it is in the list.
        """
        self.value = value
        self.weight = weight

    def __str__(self):
        if self.value is None:
            raise RuntimeError("whhhhaaaat")
        return "%s | value: %f | weight: %f" % (self.__class__.__name__, self.value, self.weight)

    def extractFromState(self, state, costs = None):
        """
        Map the state onto the feature space (i.e. a real number).
        Gets the value, doesn't update it.
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
    """

    def extractFromState(self, state, costs):
        pos = state.getPacmanPosition()
        capsules = state.getCapsules()

        # if there are capsules, return the minimum distance to a capsule
        if len(capsules) > 0:
            # caps_dists = [Astar(state, pos, c, layout) for c in capsules]
            caps_dists = [manhattanDistance(pos, c) for c in capsules]
            return min(caps_dists)
        # otherwise, return a distance slightly larger than any distance for an extant thing
        else:
            # return Astar(state, pos, (1, 1), state.data.layout)
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height))


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
