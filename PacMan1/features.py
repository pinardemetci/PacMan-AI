from util import manhattanDistance

class Feature(object):
	def __init__(self, index):
		"""
		Follwing the same pattern as Agent; the index is for the 
		Agent object to know which one it is in the list.
		"""
		self.index = index
		self.weight=0
		self.value=0

	def extractFromState(self, state):
		"""
		Map the state onto the feature space (i.e. a real number).
		"""
		raise NotImplementedError

class NearestCapsuleFeature(Feature):
	def __init__(self, index):
		super(Feature, self).__init__()
		self.weight = 0

	def extractFromState(self, state):
		pos = state.getPacmanPosition()
		capsules = state.getCapsules()

		# if there are capsules, return the minimum distance to a capsule
		if len(capsules) > 0:
			caps_dists = [manhattanDistance(pos, c) for c in capsules]
			self.value = min(caps_dists)
		# otherwise, return 0 (this could be a bad idea)
		else:
			self.value=0
		return self.value

class NearestGhostFeature(Feature):
	def __init__(self, index):
			super(Feature, self).__init__()
			self.weight = 0

	def extractFromState(self, state):
		pos = state.getPacmanPosition()
		ghosts = state.getGhostPositions()

		# if there are ghosts, return the minimum distance to a ghost
		if len(ghosts) > 0:
			ghost_dists = [manhattanDistance(pos, g) for g in ghosts]
			self.value= min(ghost_dists)
		# otherwise, return 0 (this could be a bad idea)
		else:
			self.value=0
		return self.value

# class TimeSinceCapsuleFeature(Feature):
# 	def __init__(self, index):
# 		super(Feature, self).__init__(index)

# 	def extractFromState(self, state):
# 		# hmm, we can't actually get this from the state
# 		pass