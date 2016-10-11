# You will implement this class
# At the minimum, you need to implement the selectNodes function
# If you override __init__ from the agent superclass, make sure that the interface remains identical as in agent;
# otherwise your agent will fail

from agent import Agent

import copy
from collections import deque
from sets import Set

class Frontier:

    def __init__(self):
        self.nodes = deque()

    def pop(self):
        return self.nodes.popleft()

    def pushback(self, x):
        self.nodes.append(x)

    def pushbacklist(self, xlist):
        for x in xlist:
            self.pushback(x)

    def pushfront(self, x):
        self.nodes.appendleft(x)

    def pushfrontlist(self, xlist):
        for x in xlist:
            self.pushfront(x)

    def empty(self):
        return not self.nodes


class MyAgent(Agent):

    def selectNodes(self, network):
        """
        select a subset of nodes (up to budget) to seed
        nodes in the network are selected *** BY THEIR INDEX ***
        """
        numNodes = network.size()

        selected = []

        # store the set of neighbors for each node
        nodeNeighbors = []
        for i in range(numNodes):
            nbrs = Set(network.getNeighbors(i))
            nbrs.add(i)
            nodeNeighbors.append(nbrs)
        
        # initialize the "Frontier"
        frontier = Frontier()

        # initialize selected nodes
        best = []
        bestVal = 0

        max_degree = network.maxDegree()
        ### your code goes here ###
        # [ NOTE: fill in where necessary ]

        frontier.pushfront(best)
        while not frontier.empty():
           
           # take the front element from the frontier
            assignment = frontier.pop()
           
            # manage frontier and branch-and-bound search
            # prune nodes (and subtrees) as needed
            options = self.expand(assignment, numNodes)
            for option in options:
                cover = self.eval(nodeNeighbors, option)
                if cover > bestVal:
                    bestVal = cover
                    best = option
                upper_bound = cover + (max_degree * (3 - len(option)))
                if upper_bound > bestVal:
                    frontier.pushfront(option)

        ### end your code ###
        
        return best

    def expand(self, assignment, numNodes):
        """
        expand a node in the tree

        returns children of this node in the search tree
        """

        #nodes = [sum(i, assignment) for i in range(numNodes) if i not in assignment]
        
        nodes = [] 
        ### your code goes here  ####
        begin = 0 if len(assignment) == 0 else max(assignment)
        for i in range(begin, numNodes):
            if i not in assignment:
                new_assignment = assignment[:]
                new_assignment.append(i)
                nodes.append(new_assignment)
        ### end your code  ###

        return nodes

    def eval(self, nodeNeighbors, x):
        """
        evaluate the value of node x
        nodeNeighbors is an auxiliary data structure
        keeping track of sets of neighbors for each node
        """

        nbrs = Set()
        for i in x:
            for j in nodeNeighbors[i]:
                nbrs.add(j)
        return len(nbrs)

    def display(self):
        print "Agent ID ", self.id
