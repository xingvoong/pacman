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
import random, util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best


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
        # a matrix
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # a pair (x, y)
        newPos = successorGameState.getPacmanPosition()
        # a list of T/F?
        newFood = successorGameState.getFood()
        #AgentsState object
        newGhostStates = successorGameState.getGhostStates()
        #AgentState object
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print("successorGameState", successorGameState)
    

      
        if successorGameState.isWin():
            return float("inf")
        elif successorGameState.isLose():
            return float("-inf")
        else:
            #the distance from the pacmac new position to the foods 
            foodDistance = []
            for food in list(newFood.asList()):
                foodDistance.append(util.manhattanDistance(food, newPos))

            ghostDistance = [util.manhattanDistance(newPos, newGhostStates[0].getPosition())]

            if len(foodDistance) != 0:
                return successorGameState.getScore() + 1/min(foodDistance)
            else:
                return successorGameState.getScore() - 1/min(ghostDistance)

            

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
    Your minimax agent
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        
        v = float("-inf")
        optimalAct = Directions.STOP
        for la in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, la)
            successorVal = self.eval(successor, 0, 1)

            if successorVal > v:
                v = successorVal
                optimalAct = la

        return optimalAct

    def maxValue(self, gameState, depth, agentIndex):
        v = float("-inf")
        successorVal = float("-inf")

        for la in gameState.getLegalActions(0):
            successorVal = self.eval(gameState.generateSuccessor(0, la), depth, 1)
            v = max(v, successorVal)
        return v

    def minValue(self, gameState, depth, agentIndex):
        v = float("+inf")
        successorVal = float("+inf")
        numGhost = gameState.getNumAgents() - 1

        for la in gameState.getLegalActions(agentIndex):
            # still more ghost value need to be calculate
            # increase the agentIndex
            if agentIndex != numGhost:
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth, agentIndex+1)
                v = min(v, successorVal)
            else:
            # increase the depth and call max
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth+1, 0)
                v = min(v, successorVal)
        return v

    def eval(self, gameState, depth, agentIndex):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)
        else:
            return self.minValue(gameState, depth, agentIndex)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        v = float("-inf")
        a = float("-inf")
        b = float("inf")
        optimalAct = Directions.STOP

        for la in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, la)
            successorVal = self.eval(successor, 0, 1, a, b)

            if successorVal > v:
                v = successorVal
                optimalAct = la
            a = max(v, a)
        return optimalAct


    def maxValue(self, gameState, depth, agentIndex, a, b):
        v = float("-inf")
        successorVal = float("-inf")

        for la in gameState.getLegalActions(0):
            successorVal = self.eval(gameState.generateSuccessor(0, la), depth, 1, a, b)
            v = max(v, successorVal)
            if v > b: return v
            a = max(v, a)
        return v

    def minValue(self, gameState, depth, agentIndex, a, b):
        v = float("+inf")
        successorVal = float("+inf")
        numGhost = gameState.getNumAgents() - 1

        for la in gameState.getLegalActions(agentIndex):
            # still more ghost value need to be calculate
            # increase the agentIndex
            if agentIndex != numGhost:
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth, agentIndex+1, a, b)
                v = min(v, successorVal)
            else:
            # increase the depth and call max
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth+1, 0, a, b)
                v = min(v, successorVal)
            if v < a: return v
            b = min(v, b)
        return v

    def eval(self, gameState, depth, agentIndex, a, b):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex, a, b)
        else:
            return self.minValue(gameState, depth, agentIndex, a, b)
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        v = float("-inf")
        optimalAct = Directions.STOP
        for la in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, la)
            successorVal = self.eval(successor, 0, 1)

            if successorVal > v:
                v = successorVal
                optimalAct = la

        return optimalAct

    def maxValue(self, gameState, depth, agentIndex):
        v = float("-inf")
        successorVal = float("-inf")

        for la in gameState.getLegalActions(0):
            successorVal = self.eval(gameState.generateSuccessor(0, la), depth, 1)
            v = max(v, successorVal)

        return v

    def expValue(self, gameState, depth, agentIndex):
        successorVal = float("-inf")
        expVal = 0
        numGhost = gameState.getNumAgents() - 1

        #the agent here is not pacman index anymore but of the ghosts as well
        for la in gameState.getLegalActions(agentIndex):
        # still more ghost value need to be calculate
            # increase the agentIndex
            if agentIndex != numGhost:
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth, agentIndex+1)
                expVal += successorVal
            else:
            # increase the depth and call max
                successorVal = self.eval(gameState.generateSuccessor(agentIndex, la), depth+1, 0)
                expVal += successorVal
        return expVal

    def eval(self, gameState, depth, agentIndex):
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)
        else:
            return self.expValue(gameState, depth, agentIndex)

def betterEvaluationFunction(currentGameState):

    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    # a pair (x, y)
    newPos = currentGameState.getPacmanPosition()
    # a list of T/F?
    newFood = currentGameState.getFood()
    #AgentsState object
    newGhostStates = currentGameState.getGhostStates()
    #AgentState object
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return float("-inf")
    else:
    #the distance from the pacmac new position to the foods
        capsules = currentGameState.getCapsules()
        capsulesDistance = [util.manhattanDistance(newPos,c) for c in capsules]

        score = currentGameState.getScore()
        foodDistance = []
        for food in list(newFood.asList()):
            foodDistance.append(util.manhattanDistance(food, newPos))

        ghostDistance = [util.manhattanDistance(newPos, newGhostStates[0].getPosition())]

        if len(foodDistance) != 0:
            score += 1/min(distance for distance in foodDistance)
        if len(ghostDistance) != 0:
            for distance in ghostDistance:
                for ghost in newGhostStates:
                    if ghost.scaredTimer>0:
                        score += 1/distance
                    else:
                        score -= 1/distance

        if len(capsulesDistance) != 0:
            score += 1/distance

        return score


# Abbreviation
better = betterEvaluationFunction
