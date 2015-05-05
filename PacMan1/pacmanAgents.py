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
    Pacman Agent using simple Q-learning algorithm for a continuous state space.
    """

    def __init__(self, fromPickle=True):
        """
        Pickling the feature weights for agent to learn from its actions in previous GameState

        Inherits from the Berkeley Agent class
        """
        if fromPickle:
            with open('features.p', 'rb') as f:
                self.features = pickle.load(f)
        else:
            self.features = [NearestCapsuleFeature(weight=-0.2), 
                NearestNormalGhostFeature(weight=0.2),
                NearestScaredGhostFeature(weight=-0.2), 
                # TotalFoodFeature(), 
                NearestFoodFeature(weight=-0.2)]
                # ScoreFeature()]

        self.tiles = {} #Dictionary to store game tiles, depends on the layout
        self.learningRate = 0.0001 #how much you adjust the weight relative to the Q-value
        self.discountFactor = 0.3 #Weight to balance instant reward with future long term awards
        self.explorationRate = 0.05 #probability that pacman will explore

        super(Agent, self).__init__()

    def getAction(self, state):
        """
        Initialize the game layout tiles when pacman is in start configuration

        input: GameState object
        output: random action, if exploring, and optimal action, if not exploring
        """
        if state.data.agentStates[0].configuration == state.data.agentStates[0].start:
            self.tiles = initializeTiles(state.data.layout)
        else:
            self.updateFeatures(state)
        action = self.getMaxQAction(state)
        if self.isExploring():
            legalActions = state.getLegalActions()
            final_action = random.choice(legalActions)
        else:
            final_action = action
        self.updateWeights(state, final_action)
        return final_action

    def getApproximateQValue(self, state):
        """
        multiply the current weight of each feature by an expected feature value
        to approximate Q-value

        input: GameState object
        output: Approximate Q value based on the feature weights, #
        """
        fs = [(f.extractFromState(state, self.tiles), f.weight) for f in self.features]
        return sum([f[0] * f[1] for f in fs])

    def getQValue(self, state, action):
        """
        Calculate the Q-Value based on algorithm
        Q' = (1-learningRate) * (Q + learningRate) * (R + R')

        input: stateObject, action as a direction 
        output: Q-value, number
        """
        currentQ = self.getApproximateQValue(state)
        nextState = state.generateSuccessor(0, action)
        currentReward = self.getExpectedNextReward(state, action)
        futureReward = self.discountFactor * self.getApproximateQValue(nextState)
        q = (1 - self.learningRate) * currentQ + self.learningRate * (currentReward + futureReward)
        return q

    def getMaxQ(self, state):
        """
        Calculate the Q-values of all the legal actions and determine max value

        input: stateObject
        output: tuple of maximum Q-value with a corresponding action
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
        input: stateObject
        output: maximum Q-Value
        """
        return self.getMaxQ(state)[1]

    def getMaxQAction(self, state):
        """
        input: stateObject
        output: action with the maximum Q-value
        """
        return self.getMaxQ(state)[0]

    def updateWeights(self, state, action):
        """
        Change weights of each feature based on the change in that
        feature from the last state.
        w_t+1 = w_t + alpha(r_t+1 + gamma* max(a)Q(s', a) - Q(s, a))*phi_t

        input: stateObject, action as a direction
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

        inpute:stateobject
        """
        for f in self.features:
            f.updateValue(state, self.tiles)

    def getExpectedNextReward(self, state, action):
        """
        Calculate the expected reward of a given state and action
        r_t+1 = R(s_t, a_t, s_t+1)

        input: stateObject, action as a direction
        output: change in score
        """
        nextState = state.generateSuccessor(0, action)
        return nextState.getScore() - state.getScore()

    def isExploring(self):
        """
        Uses explorationRate to decide if we explore or not.
        """
        r = random.random()
        if r < self.explorationRate:
            return True
        else:
            return False

    def lose(self, state):
        """
        Update the feature weights and store when lose

        input: stateObject
        output: feature weights in pickle file
        """
        expectedReward = state.data.scoreChange
        currentQ = self.getApproximateQValue(state)
        print "Pickling"
        for f in self.features:
            f.weight = f.weight + self.learningRate * (expectedReward - currentQ) * f.value
        pickle.dump(self.features, open('features.p', 'wb'))

    def win(self, state):
        """
        Update the feature weights and store when won

        input: stateObject
        output: feature weights in pickle file
        """
        expectedReward = state.data.scoreChange
        currentQ = self.getApproximateQValue(state)
        print "Pinkling"
        for f in self.features:
            f.weight = f.weight + self.learningRate * (expectedReward - currentQ) * f.value
        pickle.dump(self.features, open('features.p', 'wb'))
