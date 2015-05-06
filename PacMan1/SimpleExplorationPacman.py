

class SimpleExplorationPacman(Agent):
    """
    A Pacman agent that uses a VERY simple q-learning algorithm in which the states
    have been encoded as "explored" and "unexplored", and Pacman can only be in one
    state (since he can't be standing in an unexplored cell). That might make it not
    actually qualify as q-learning, but you know, baby steps.
    """
    def __init__(self):
        super(Agent, self).__init__()  # call the parent's init function
        self.Q = [0, 0]  # Q always initializes with zeros
        self.R = [1, 5]  # hard-coding R for now
        self.gamma = 0.3  # exploration parameter
        self.exploredCoords = set()  # set of coordinates Pacman has been to

    def getAction(self, state):
        """
        Any Agent subclass must define a getAction method.

        state: the GameState object
        returns: the direction PacMan should go (e.g. Directions.NORTH)
        """

        # add current position to exploredCoords
        self.exploredCoords.add(state.getPacmanPosition())

        rewards = self.getActionRewards(state, state.getLegalActions())

        if self.goRandomDirection():
            direction = random.choice(state.getLegalActions())
            directionReward = rewards[direction]
        else:
            direction, directionReward = max(rewards.iteritems(), key=operator.itemgetter(1))  # this currently biases toward last option, probably East

        self.updateQ(state, self.Q.index(directionReward), set(rewards.values()))

        return direction

    def getReward(self, state, action):
        """
        Checks the Q matrix to see what we've got.

        Eventually we'll need a mapping between thes=        """
        # if it's explored, return the "explored" Q value
        if state.generatePacmanSuccessor(action).getPacmanPosition() in self.exploredCoords:
            return self.Q[0]
        # otherwise return the "unexplored" Q value
        else:
            return self.Q[1]

    def getActionRewards(self, state, legalActions):
        """
        Return a dictionary like {direction: reward} for all legal directions
        """
        reward = dict.fromkeys(legalActions)
        for action in legalActions:
            reward[action] = self.getReward(state, action)
        return reward

    def updateQ(self, state, newState, legalActions):
        """
        Update the Q matrix (brain) of our PacMan with
        Q(currentState, newState) = R(currentState, newState) + gamma * max(Q(newState, legalActions))

        state: the GameState object
        newState: 0 or 1 (explored or unexplored) -- sorry this is confusing
        legalActions: [0] or [0, 1] depending on if any unexplored cells are legally moveable-to
        """
        self.Q[newState] = self.R[newState] + self.gamma * max(filter(lambda x: x in legalActions, self.Q))
        print "updated Q: ", self.Q

    def goRandomDirection(self):
        """
        Should it go with the highest Q value or try something new?

        returns: boolean
        """
        r = random.random()
        if r > self.gamma:
            return True
        else:
            return False