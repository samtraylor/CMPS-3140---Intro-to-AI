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

        "*** YOUR CODE HERE ***"
        remaining_food = newFood.asList()
        F_Dist = []
        for food in remaining_food:
            F_Dist.append(manhattanDistance(food, newPos))
        #Make list of ghost distances
        ghost_locations = successorGameState.getGhostPositions()
        G_Dist = []
        for ghost_location in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost_location) <2):
                return -float('inf')
        if len(F_Dist) == 0:
            return float('inf')

        return 1000/sum(F_Dist) + 10000/len(F_Dist)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"


        def maxVal(gameState, agentIndex, depth):
            agentIndex = 0
            actions = gameState.getLegalActions(agentIndex)

            if len(actions) == 0 or self.depth == depth:
                return self.evaluationFunction(gameState)

            val = max(minVal(gameState.generateSuccessor(agentIndex,i), agentIndex + 1, depth + 1) for i in actions)
            #maxim = max(minValue(state.generateSuccessor(agentIndex, action),agentIndex + 1, depth + 1) for action in legalActions)
            return val

        def minVal(gameState, agentIndex, depth):
            agentCount = gameState.getNumAgents()
            #successors = [gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex)]
            actions = gameState.getLegalActions(agentIndex)
            pacManNext = False 

            if agentIndex == agentCount - 1:
                pacManNext = True
        
            if len(actions) == 0:
                return self.evaluationFunction(gameState)
            
            if pacManNext:
                val = min(maxVal(gameState.generateSuccessor(agentIndex,i),agentIndex,depth) for i in actions)
            else:
                #print("taking min between ", val, "and", maxVal(i,))
                val = min(minVal(gameState.generateSuccessor(agentIndex,i),agentIndex + 1, depth) for i in actions)
                #print("min found as", val)
            return val    
 
        actions = gameState.getLegalActions(0)
        pairs = {}
        for action in actions:
            pairs[action] = minVal(gameState.generateSuccessor(0, action), 1, 1)

        bestUtility = max(pairs.values())

        for action,utility in pairs.items():
            if utility == bestUtility:
                return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def maxVal(gameState, agentIndex, depth, alpha, beta):
            localMax = -99999
            agentIndex = 0
            actions = gameState.getLegalActions(agentIndex)
            runningAlpha = alpha

            if len(actions) == 0 or self.depth == depth:
                return self.evaluationFunction(gameState)

            for i in actions:
                localMax = max(localMax,minVal(gameState.generateSuccessor(agentIndex,i), agentIndex + 1, depth + 1, runningAlpha, beta))
                if localMax > beta:
                    return localMax
                runningAlpha = max(localMax, runningAlpha)

            return localMax

        def minVal(gameState, agentIndex, depth,alpha, beta):
            localMin = 99999
            agentCount = gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            runningBeta = beta 

            if len(actions) == 0:
                return self.evaluationFunction(gameState)
            
            if agentIndex == agentCount - 1:
                for i in actions:
                    localMin = min(localMin,maxVal(gameState.generateSuccessor(agentIndex,i),agentIndex,depth, alpha, runningBeta))
                    if localMin < alpha:
                        return localMin
                    runningBeta = min(localMin,runningBeta)

            else:
                #print("taking min between ", val, "and", maxVal(i,))
                for i in actions:
                    localMin = min(localMin,minVal(gameState.generateSuccessor(agentIndex,i),agentIndex + 1, depth,alpha, runningBeta))
                    if localMin < alpha:
                        return localMin
                    runningBeta = min(localMin,runningBeta)
                #print("min found as", val)  
            return localMin
 
        initBeta = 99999
        initAlpha = -99999
        actions = gameState.getLegalActions(0)
        pairs = {}
        for action in actions:
            pairs[action] = minVal(gameState.generateSuccessor(0, action), 1, 1, initAlpha, initBeta)
            #print("pairs now", pairs)

            if pairs[action] > initBeta:
                return action
            initAlpha = max(pairs[action],initAlpha)

        bestUtility = max(pairs.values())

        for action,utility in pairs.items():
            if utility == bestUtility:
                return action
        


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
        "*** YOUR CODE HERE ***"
        def maxVal(gameState, agentIndex, depth):
            agentIndex = 0
            actions = gameState.getLegalActions(agentIndex)

            if len(actions) == 0 or self.depth == depth:
                return self.evaluationFunction(gameState)

            val = max(expectiMax(gameState.generateSuccessor(agentIndex,i), agentIndex + 1, depth + 1) for i in actions)
            #maxim = max(minValue(state.generateSuccessor(agentIndex, action),agentIndex + 1, depth + 1) for action in legalActions)
            return val

        def expectiMax(gameState, agentIndex, depth):
            agentCount = gameState.getNumAgents()
            successors = [gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex)]
            actions = gameState.getLegalActions(agentIndex)
            avgUtil = 0

            if len(actions) == 0:
                return self.evaluationFunction(gameState)
            else:
                distribution = 1.0 / len(actions)
            
            for i in actions:
                if agentIndex == agentCount - 1:
                    avgUtil += maxVal(gameState.generateSuccessor(agentIndex,i),agentIndex,depth) * distribution
                else:
                    avgUtil += expectiMax(gameState.generateSuccessor(agentIndex,i),agentIndex + 1, depth) * distribution
            return avgUtil
 
        actions = gameState.getLegalActions(0)
        pairs = {}
        for action in actions:
            pairs[action] = expectiMax(gameState.generateSuccessor(0, action), 1, 1)

        bestUtility = max(pairs.values())

        for action,utility in pairs.items():
            if utility == bestUtility:
                return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pac_location = currentGameState.getPacmanPosition()
    food_proximity = [manhattanDistance(pac_location, food_locations) for food_locations in currentGameState.getFood().asList()]
    ghost_location = currentGameState.getGhostPositions()
    ghost_list = currentGameState.getGhostStates()
    power_pellets_remaining = len(currentGameState.getCapsules())
    total = 0
    scared = False
    #minfooddist = 1

    
    if len(food_proximity)>0:
        minfooddist = min(food_proximity)
    #Prioritize food unless the ghosts get too close
    
    for ghost in ghost_location:
        ghost_dist = manhattanDistance(pac_location, ghost)
        if ghost_dist <= 2 and scared == False:
            return -float("inf")
    ghosts = ghost_list[0]
    if ghosts.scaredTimer > 0:
        scared_dist = [manhattanDistance(pac_location, ghosts.getPosition())]
        total += ((1.0 / float(scared_dist[0]))*102)
        scared = True
    else:
        scared = False

    if len(food_proximity) > 0:
        total += ((1.0 / len(food_proximity))* 1000000)
        total += ((1.0 / minfooddist) * 1)
    if power_pellets_remaining > 0:
        total += ((1.0 / power_pellets_remaining)*20000)

    if currentGameState.isWin():
        total+= float("inf")
        return total
    elif currentGameState.isLose():
        total += float("-inf")
        return total

    return total
# Abbreviation
better = betterEvaluationFunction
