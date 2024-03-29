# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
       
        for i in range(self.iterations):
            vState = util.Counter()  
            for state in self.mdp.getStates():
              vActions = util.Counter()
              for a in self.mdp.getPossibleActions(state):
                vActions[a] = self.computeQValueFromValues(state, a)
              vState[state] = vActions[vActions.argMax()]
            # need to do it with a new for loop, with the same iterations
            for state in self.mdp.getStates():
              self.values[state] = vState[state]
            

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qValue = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
          reward = self.mdp.getReward(state, action, nextState)
          qValue += prob * (reward + self.discount*self.values[nextState])
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
      
        #maxValue = float('inf')
        #bestAct = None
        if len(self.mdp.getPossibleActions(state)) != 0:
          vActions = util.Counter()
          for a in self.mdp.getPossibleActions(state):
            vActions[a] = self.computeQValueFromValues(state, a)
          return vActions.argMax()
        else:
          return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
      
      for i in range(self.iterations):
        vState = util.Counter()
        state = self.mdp.getStates()[i% len(self.mdp.getStates())]
        vActions = util.Counter()
        for a in self.mdp.getPossibleActions(state):
          vActions[a] = self.computeQValueFromValues(state,a)
        vState[state] = vActions[vActions.argMax()]
        self.values[state] = vState[state]



class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
       
        #Compute predecessors of all states
        # a set of predecessors 
        predecessors = {}
        for s in self.mdp.getStates():
          for a in self.mdp.getPossibleActions(s):
            for ns, prob in self.mdp.getTransitionStatesAndProbs(s, a):
              if ns not in predecessors:
                predecessors[ns] = {s}
              else:
                predecessors[ns].add(s) 
                
                
        #Initialize an empty priority queue.
        PQ = util.PriorityQueue()

        #For each non-terminal state s, do:....
        for s in self.mdp.getStates():
          if not self.mdp.isTerminal(s):
            qValues = []
            for a in self.mdp.getPossibleActions(s):
              qValue = self.computeQValueFromValues(s,a)
              qValues.append(qValue)
            diff = abs(max(qValues)- self.values[s])
            PQ.update(s, -diff)

        #For iteration in 0, 1, 2, ..., self.iterations - 1, do: ... 
        for i in range(self.iterations):
          if PQ.isEmpty():
            break

          popState = PQ.pop()
          qValues = []
          for a in self.mdp.getPossibleActions(popState):
            qValue = self.computeQValueFromValues(popState,a)
            qValues.append(qValue)
          self.values[popState] = max(qValues)

          for p in predecessors[popState]:
            qValues = []
            for a in self.mdp.getPossibleActions(p):
              qValue = self.computeQValueFromValues(p,a)
              qValues.append(qValue)
            diff = abs(max(qValues)- self.values[p])
            if diff > self.theta:
              PQ.update(p, -diff)


