import random
from util import manhattanDistance

class Feature(object):
	def __init__(self, value=0, weight=0):
		"""
		Follwing the same pattern as Agent; the index is for the 
		Agent object to know which one it is in the list.
		"""
		self.value = value
		self.weight = weight

	def extractFromState(self, state):
		"""
		Map the state onto the feature space (i.e. a real number).
		"""
		raise NotImplementedError

class NearestCapsuleFeature(Feature):
	def __init__(self, weight=random.random()):
		super(Feature, self).__init__()
		# wtf python
		# these next two lines shouldn't be necessary if I use super()
		self.value = random.random()
		self.weight = weight

	def extractFromState(self, state):
		pos = state.getPacmanPosition()
		capsules = state.getCapsules()

		# if there are capsules, return the minimum distance to a capsule
		if len(capsules) > 0:
			caps_dists = [manhattanDistance(pos, c) for c in capsules]
			return min(caps_dists)
		# otherwise, return 0 (this could be a bad idea)
		else:
			return 0

	def updateValue(self, state):
		self.value = self.extractFromState(state)

	def __str__(self):
		return "Nearest Capsule: " + str(self.value)

class NearestGhostFeature(Feature):
	def __init__(self, weight=random.random()):
			super(Feature, self).__init__()
			self.value = random.random()
			self.weight = weight

	def extractFromState(self, state):
		pos = state.getPacmanPosition()
		ghosts = state.getGhostPositions()

		# if there are ghosts, return the minimum distance to a ghost
		if len(ghosts) > 0:
			ghost_dists = [manhattanDistance(pos, g) for g in ghosts]
			return min(ghost_dists)
		# otherwise, return 0 (this could be a bad idea)
		else:
			return 0

	def updateValue(self, state):
		self.value = self.extractFromState(state)

	def __str__(self):
		return "Nearest Ghost: " + str(self.value)

# class TimeSinceCapsuleFeature(Feature):
# 	def __init__(self, index):
# 		super(Feature, self).__init__(index)

# 	def extractFromState(self, state):
# 		# hmm, we can't actually get this from the state
# 		pass