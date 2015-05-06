"""
@authors: Kelly Brennan, Stephanie Norway and Pinar Demetci
All of the possible features that can be incorporated into Q-learning algorithm
"""

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

    def extractFromState(self, state, costs=None):
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
        return: (float) if capsules present, return minimum distance to capsule
            otherwise return the manhattanDistance of the layout board, making pacman think they are far away 
        """
        pos = state.getPacmanPosition()
        capsules = state.getCapsules()

        if len(capsules) > 0:
            caps_dists = [Astar(state, pos, c, state.data.layout, costs) for c in capsules]
            return min(caps_dists)
        else:
            return manhattanDistance((0, 0), (state.data.layout.width, state.data.layout.height)) 


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
        return: (float) if normal ghosts present, return minimum distance to normal ghost
            otherwise return the manhattanDistance of the layout board, making pacman think they are far away
        """
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
    Distance to the nearest scared ghost after PacMan eats a capsule.
    Implements Astar search algorithm
    """

    def extractFromState(self, state, costs):
        """
        determine distance between pacman and a scared ghost

        state: GameState object
        costs: tile object of game layout
        return: (float) if scared ghosts present, return minimum distance to scared ghost
            otherwise return the manhattanDistance of the layout board, making pacman think they are far away
        """
        pos = state.getPacmanPosition()
        ghosts = state.getGhostStates()
        scared_ghosts = filter(lambda g: g.scaredTimer > 0, ghosts)  # filters the ones that are in scared time.
        # After PacMan eats a capsule, scared time starts.
        if len(scared_ghosts) > 0:
            scared_ghost_dists = [Astar(state, pos, s.getPosition(), state.data.layout, costs) for s in scared_ghosts]
            return min(scared_ghost_dists)
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
        return: number of total food on the board (float)
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
        return: (float) if food exists, manhattanDistance to nearest food pellet
            otherwise, return 0 (Game has been won)
        """
        pos = state.getPacmanPosition()
        if state.getNumFood() > 0:
            foodDistances = [manhattanDistance(pos, f) for f in state.getFood().asList()]
            return min(foodDistances)
        else:
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
        return: weighted score (float)
        """
        return state.getScore() * 0.01  # multiply constant to manage weight values from becoming exceedingly large
