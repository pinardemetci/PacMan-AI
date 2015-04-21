class Action(object):
	"""
	Generic class from which we can subclass specific
	"actions" aka goals
	"""

	# def __init__(self, index):
	# 	"""
	# 	The index argument will be for indexing into the array...
	# 	"""
	# 	self.index = index

	def execute(self, state):
		"""
		Much like the Berkeley people wrote Agent, an Action must define
		its execution function. 
		"""
		raise NotImplementedError

class AstarAction(Action):
	"""
	The action class for performing the AStar search.
	This will tell Pacman to go to a specific location,
	specified by the goalPos argument.
	"""
	# def __init__(self, index, goalPos):
		# super(Action, self).__init__(index)
	def __init__(self, goalPos):
		self.goalPos = goalPos

	def execute(self, state):
		pass

class RunawayAction(Action):
	"""
	Sometimes the best thing to do is GTFO
	"""

	def execute(self, state):
		pass