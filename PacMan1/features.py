import random
from util import manhattanDistance
from util2 import * #imports A-star algorithm
 

class Feature(object):
    def __init__(self, value=random.random(), weight=random.random()):
        """
        Main class for the features that we use for Q iteration with value approximation. 
        Following the same pattern as Agent; the index is for the Agent object 
        to know which feature it is in the features list.
        """
        # Value of the feature will be used to compute Q values and weight updates. Starts with random until updated for the first time
        self.value = value   
        # Weight of the feature. This is also used in Q values. It determines which features are prioritized and affects the agent's moves.
        self.weight = weight  

    def __str__(self):
        """
        Returns the name, value and weight of the feature so that it's easy to track updates in the command line.
        """
        return "%s | value: %f | weight: %f" % (self.__class__.__name__, self.value, self.weight)

    def extractFromState(self, state, costs = None):
        """
        Map the state onto the feature space (i.e. a real number).
        Gets the value, doesn't update it.
        It will be implemented for each feature we create.
        Raises an error in case we forget to implement.
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
    Calculates the distance to the nearest capsule.
    Inherits from the main Feature class, like every other feature.
    """

    def extractFromState(self, state, costs):
        """
        Uses A-star algorithm to calculate the distance to the nearest capsule. 
        A-star algorithm we implemented is in util2.py file.
        """
        pos = state.getPacmanPosition() #position of the PacMan
        capsules = state.getCapsules() # position of all capsules

        # if there are capsules, return the minimum distance to a capsule.
        if len(capsules) > 0:
            # caps_dists = [Astar(state, pos, c, layout) for c in capsules]
            caps_dists = [manhattanDistance(pos, c) for c in capsules]
            return min(caps_dists)
        # otherwise, returns the largest distance possible in the layout
        else:
            return manhattanDistance((0,0), (state.data.layout.width, state.data.layout.height)) 

class NearestNormalGhostFeature(Feature):
    """
    Feature for Ghosts in non-scared time. 
    Inherits from the Feature class.
    Gives the distance to the nearest non-scared ghost.
    """

    def extractFromState(self, state, costs):
        """
        Uses A-star algorithm to calculate the distance to the nearest non-scared ghost.
        Otherwise, returns the largest manhattanDistance
        """
        pos = state.getPacmanPosition() #position of PacMan
        ghosts = state.getGhostStates() #States of all the ghosts
        normal_ghosts = filter(lambda g: g.scaredTimer == 0, ghosts) #filters the non-scared ghosts only.

        #If there are ghosts in the layout, return A-star to the nearest one
        if len(normal_ghosts) > 0:
            normal_ghost_dists = [Astar(state, pos, n.getPosition(), state.data.layout, costs) for n in normal_ghosts]
            return min(normal_ghost_dists)
        else:
        #If not, returns the largest distance possible in the layout
            return manhattanDistance((0,0), (state.data.layout.width, state.data.layout.height))

class NearestScaredGhostFeature(Feature):
    """
    Feature for the Scared Ghosts for when PacMan eats the capsule and scared time starts
    Distance to the nearest scared ghost.
    """

    def extractFromState(self, state, costs):
        """
        Uses A-star for the nearest scared ghost. 
        If non exists, returns the largest distance possible by using manhattanDistance
        """
        pos = state.getPacmanPosition() #Position of the PacMan
        ghosts = state.getGhostStates() #States of the all the ghosts in the layout
        scared_ghosts = filter(lambda g: g.scaredTimer > 0, ghosts) #Filters the scared ghosts only.

        #If scared ghosts exist:
        if len(scared_ghosts) > 0:
            #Return A-star value
            scared_ghost_dists = [Astar(state, pos, s.getPosition(), state.data.layout, costs) for s in scared_ghosts]
            return min(scared_ghost_dists)
        #If there are non scared ghosts:
        else:
            # returns the largest distance possible in the layout
           return manhattanDistance((0,0), (state.data.layout.width, state.data.layout.height))


class TotalFoodFeature(Feature):
    """
    Feature for Total Number of Food. Inherits from the main Feature class. 
    """

    def extractFromState(self, state, costs):
        """
        Returns the total number of food remaining on the board
        """
        return state.getNumFood()


class NearestFoodFeature(Feature):
    """
    PacMan's distance to nearest food. Inherits from 'Feature'
    Uses manhattanDistance 
    """

    def extractFromState(self, state, costs):
        """
        Uses manhattanDistance instead of A-star to speed the process up.
        """
        pos = state.getPacmanPosition() #position of the PacMan
        food = state.getFood() #State of the food

        if state.getNumFood() > 0: 
            foodDistances = [manhattanDistance(pos, f) for f in food] #manhattanDistance to each food
            return min(foodDistances) #return the nearest one
        else: #if all food is eaten, return the largest distance possible to act like food is just really far away.
            return manhattanDistance((0,0), (state.data.layout.width, state.data.layout.height)) 
