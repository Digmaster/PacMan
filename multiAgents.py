# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys
from pacman import GhostRules

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"


		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		newScore = successorGameState.getScore()

		if successorGameState.isLose():
			return newScore-1000
		if successorGameState.isWin():
			return newScore+1000

		if(max(newScaredTimes)==40):
			newScore = newScore + 40 #Weigh scores here we score a super pellet highly

		for i in range(len(newGhostStates)):
			ghost = newGhostStates[i]

			#ignore ghosts you can eat
			if(ghost.scaredTimer!=0):
				continue

			i = i+1
			newScore = newScore + ghost.scaredTimer

			# Check if the ghost can move into our square in the next turn
			for ghostAction in GhostRules.getLegalActions(successorGameState, i):
				ghostSuccessor = successorGameState.generateSuccessor(i, ghostAction)
				if ghostSuccessor.getGhostState(i).getPosition() == newPos:
					return newScore-1000

		if(len(currentGameState.getFoodCoords())==len(successorGameState.getFoodCoords())):
			newScore = newScore - successorGameState.getClosestFood(newPos)[2]

		return newScore

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.decideMove(gameState, 0, gameState.getNumAgents()*self.depth, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def decideMove(self, gameState, player, depth, action):
		gameState = gameState.generateSuccessor(player, action)
		if gameState.isWin() or gameState.isLose(): # test for a winning solution to the current state
			return self.evaluationFunction(gameState)

		depth = depth-1

		player = (player+1)%gameState.getNumAgents()

		if(depth == 0):
			return self.evaluationFunction(gameState)

		if player==0:
			legalMoves = gameState.getLegalActions()

			# Choose one of the best actions
			scores = [self.decideMove(gameState, 0, depth, action) for action in legalMoves]

			bestScore = max(scores)
			bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
			chosenIndex = random.choice(bestIndices) # Pick randomly among the best

			return bestScore;
		else:
			legalMoves = gameState.getLegalActions(player)

			# Choose one of the best actions
			scores = [self.decideMove(gameState, player, depth, action) for action in legalMoves]

			bestScore = min(scores)
			bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
			chosenIndex = random.choice(bestIndices) # Pick randomly among the best

			return bestScore;



class AlphaBetaAgent(MultiAgentSearchAgent):	
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""
	
	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		v = -9999
		best = v
		bestAction = Directions.STOP
		alpha = -9999
		beta = 9999
		for action in legalMoves:
			v = self.decideMove(gameState, 0, gameState.getNumAgents()*self.depth-1, action, alpha, beta)

			if v > alpha:
				alpha = v

			if v > best:
				best = v
				bestAction = action

			if beta < alpha:
				return best

		#chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return bestAction

	def decideMove(self, gameState, player, depth, action, alpha, beta):
		gameState = gameState.generateSuccessor(player, action)
		if gameState.isWin() or gameState.isLose() or depth == 0: # test for a winning solution to the current state
			return self.evaluationFunction(gameState)

		player = (player+1)%gameState.getNumAgents()

		if player==0:
			legalMoves = gameState.getLegalActions(player)

			# Choose one of the best actions
			v = -9999
			best = v
			for action in legalMoves:
				v = self.decideMove(gameState, player, depth-1, action, alpha, beta)

				if v > alpha:
					alpha = v

				if v > best:
					best = v

				if beta < alpha:
					return best
			return best
		else:
			legalMoves = gameState.getLegalActions(player)

			# Choose one of the best actions
			v = 9999
			best = v
			for action in legalMoves:
				v = self.decideMove(gameState, player, depth-1, action, alpha, beta)

				if v < beta:
					beta = v

				if v < best:
					best = v

				if beta < alpha:
					return best
			return best

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		v = -9999
		best = v
		bestAction = Directions.STOP
		for action in legalMoves:
			v = self.decideMove(gameState, 0, gameState.getNumAgents()*self.depth-1, action)
			if v > best:
				best = v
				bestAction = action

		return bestAction

	def decideMove(self, gameState, player, depth, action):
		gameState = gameState.generateSuccessor(player, action)
		if gameState.isWin() or gameState.isLose() or depth == 0: # test for a winning solution to the current state
			return self.evaluationFunction(gameState)

		player = (player+1)%gameState.getNumAgents()

		if player==0:
			legalMoves = gameState.getLegalActions(player)

			# Choose one of the best actions
			v = -9999
			best = v
			for action in legalMoves:
				v = self.decideMove(gameState, player, depth-1, action)
				if v > best:
					best = v
			return best
		else:
			legalMoves = gameState.getLegalActions(player)

			scores = [self.decideMove(gameState, player, depth-1, action) for action in legalMoves]
			return sum(scores)/len(scores)


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	# Useful information you can extract from a GameState (pacman.py)
	newPos = currentGameState.getPacmanPosition()
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	newScore = currentGameState.getScore()

	if currentGameState.isLose():
		return newScore-1000
	if currentGameState.isWin():
		return newScore+1000

	#if(max(newScaredTimes)==40):
	newScore = newScore + max(newScaredTimes)*1000 #Weigh scores here we score a super pellet highly

	ghostDistance = 0
	for i in range(len(newGhostStates)):
		ghost = newGhostStates[i]

		#ignore ghosts you can eat
		if(ghost.scaredTimer!=0):
			ghostDistance -= manhattanDistance(ghost.getPosition(), newPos);
			continue

		i = i+1
		newScore = newScore + ghost.scaredTimer
		if(manhattanDistance(ghost.getPosition(), newPos) < 10):
			ghostDistance += manhattanDistance(ghost.getPosition(), newPos);

		# Check if the ghost can move into our square in the next turn
		for ghostAction in GhostRules.getLegalActions(currentGameState, i):
			ghostSuccessor = currentGameState.generateSuccessor(i, ghostAction)
			if ghostSuccessor.getGhostState(i).getPosition() == newPos:
				return newScore-1000

	# if(len(currentGameState.getFoodCoords())==len(currentGameState.getFoodCoords())):
	#newScore = newScore - currentGameState.getClosestFood(newPos)[2]
	newScore += ghostDistance/10;

	return newScore

# Abbreviation
better = betterEvaluationFunction

