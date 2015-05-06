"""
Glue for interfacing with the Berkeley code.
@author Stephanie Northway, Kelly Brennan and Pinar Demetci
"""

import operator
import random
import pickle

from game import Agent, Directions
from features import *
from util2 import initializeTiles


class SimpleQPacman(Agent):
    """
    Represents the pacman agent that implements the continuous state Q-learning
    algorithm to learn from it's previous exerience. The agent inherits the
    attritbutes and methods from the Berkeley Agent Class.

    features: a list of Features the agent will use
    tiles: dictionary to hold all of the tiles on the game layout
    learningRate: how much you adjust the weight relative to the Q-value
    discountFactor: Weight to balance instant reward with future long term awards
    exploraitonRate: probability that pacman will explore, instead of using optimal action
    """

    def __init__(self, fromPickle=True):
        """
        Pickling the feature weights for agent to learn from its actions in previous GameState
        """
        if fromPickle:
            with open('features.p', 'rb') as f:
                self.features = pickle.load(f)
        else:
            self.features = [
                NearestCapsuleFeature(weight=-0.2),
                NearestNormalGhostFeature(weight=0.2),
                NearestScaredGhostFeature(weight=-0.2),
                # TotalFoodFeature(),
                NearestFoodFeature(weight=-0.2),
                # ScoreFeature()
            ]

        self.tiles = {}
        self.learningRate = 0.0001
        self.discountFactor = 0.3
        self.explorationRate = 0.05

        super(Agent, self).__init__()

    def getAction(self, state):
        """
        getAction runs pacman agent's show by determing what action the 
        agent will take, based on it's current state and Q-learning values

        Initialize the game layout tiles when pacman is in start configuration
        Updates the pacman's feature values
        Determines the agent's optimal action, given its specific configuration
        based on the maximum Q value or implements a random action
        Updates feature weights based on it's final action

        state: GameState object
        returns: random action, if exploring, and optimal action, if not exploring
        """
        if state.data.agentStates[0].configuration == state.data.agentStates[0].start:
            self.tiles = initializeTiles(state.data.layout)
        else:
            self.updateFeatures(state)
        if self.isExploring():
            legalActions = state.getLegalActions()
            final_action = random.choice(legalActions)
        else:
            action = self.getMaxQAction(state)
            final_action = action
        self.updateWeights(state, final_action)
        return final_action

    def getApproximateQValue(self, state):
        """
        Calculate the linear combination of the feature values and their
        respective weights to approximate Q-value.

        state: GameState object
        return: Approximate Q value based on the feature weights, #
        """
        fs = [(f.extractFromState(state, self.tiles), f.weight) for f in self.features]
        return sum([f[0] * f[1] for f in fs])

    def getQValue(self, state, action):
        """
        Calculate the Q-Value based on algorithm
        Q' = (1-learningRate) * (Q + learningRate) * (R + R')

        state: GameState object
        action: direction (string)
        return: Q-value (float)
        """
        currentQ = self.getApproximateQValue(state)
        nextState = state.generateSuccessor(0, action)
        currentReward = self.getExpectedNextReward(state, action)
        futureReward = self.discountFactor * self.getApproximateQValue(nextState)
        q = (1 - self.learningRate) * currentQ + self.learningRate * (currentReward + futureReward)
        return q

    def getMaxQ(self, state):
        """
        Calculate the Q-values of all the legal actions and determine max Q-value
        to determine the optimal action

        state: GameState object
        return: action, maximum Q-value (tuple: string, float)
        """
        if state.isWin() or state.isLose():
            return (Directions.STOP, self.getApproximateQValue(state))
        else:
            legalActions = state.getLegalActions()
            actionValuePairs = []
            for a in legalActions:
                actionValuePairs.append((a, self.getQValue(state, a)))
            return max(actionValuePairs, key=operator.itemgetter(1))

    def getMaxQValue(self, state):
        """
        return max Q-value of given agent state

        state: GameState object
        return: maximum Q-Value (float)
        """
        return self.getMaxQ(state)[1]

    def getMaxQAction(self, state):
        """
        return action with max Q-value of given agent state

        state: GameState object
        return: action with the maximum Q-value (string)
        """
        return self.getMaxQ(state)[0]

    def updateWeights(self, state, action):
        """
        Essential for pacman learning what features are most important for earning rewards
        negative weight values - pacman attracted toward feature to increase reward
            ex. agent going towards food
        positive weight values - pacman repelled by feature to increase reward
            ex. agent going away from ghosts

        update weight values of each feature based on the change in that
        feature from the last state.
        w_t+1 = w_t + alpha(r_t+1 + gamma* max(a)Q(s', a) - Q(s, a))*phi_t

        state: GameState object,
        action: direction (string)
        return: None
        """
        nextState = state.generateSuccessor(0, action)
        expectedReward = self.getExpectedNextReward(state, action)
        discountedFutureQ = self.discountFactor * self.getMaxQValue(nextState)
        currentQ = self.getQValue(state, action)
        for f in self.features:
            f.weight = f.weight + self.learningRate * (expectedReward + discountedFutureQ - currentQ) * f.value

    def updateFeatures(self, state):
        """
        Update the feature values

        state: GameState object
        returns: None
        """
        for f in self.features:
            f.updateValue(state, self.tiles)
            print f

    def getExpectedNextReward(self, state, action):
        """
        More reward is given when pacman agent increases the score with it's action
        Calculate the expected reward of a given state and action based on score change
        r_t+1 = R(s_t, a_t, s_t+1)

        state: GameState object
        Action: direction (string)
        return: change in score based on action
        """
        nextState = state.generateSuccessor(0, action)
        return nextState.getScore() - state.getScore()

    def isExploring(self):
        """
        Uses explorationRate to decide if pacman agent explores or uses Q-learning

        returns: True or False
        """
        r = random.random()
        if r < self.explorationRate:
            return True
        else:
            return False

    def lose(self, state):
        """
        Stores feature weight values when game ends so pacman agent can learn from experience
        over multiple games
        Update the feature weights and store by pickling when pacman agent loses

        input: GameState object
        output: feature weights in pickle file
        """
        expectedReward = state.data.scoreChange
        currentQ = self.getApproximateQValue(state)
        for f in self.features:
            f.weight = f.weight + self.learningRate * (expectedReward - currentQ) * f.value
        pickle.dump(self.features, open('features.p', 'wb'))

    def win(self, state):
        """
        Stores feature weight values when game ends so pacman agent can learn from experience
        over multiple games
        Update the feature weights and store by pickling when pacman agent wins

        input: GameState object
        output: feature weights in pickle file
        """
        expectedReward = state.data.scoreChange
        currentQ = self.getApproximateQValue(state)
        for f in self.features:
            f.weight = f.weight + self.learningRate * (expectedReward - currentQ) * f.value
        pickle.dump(self.features, open('features.p', 'wb'))
