# You will implement this class
# At the minimum, you need to implement the selectNodes function
# If you override __init__ from the agent superclass, make sure that the interface remains identical as in agent;
# otherwise your agent will fail

from agent import Agent

from collections import deque
import copy
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
        assignments = []
        for i in range(numNodes):
            assignments.append(0)

        best = tuple(assignments)
        bestVal = 0

        max_degree = 0
        ### your code goes here ###
        # [ NOTE: fill in where necessary ]

        for i in range(numNodes):
            if network.degree(i) > max_degree:
                max_degree = network.degree(i)
    

        frontier.pushfront(best)
        count = 0
        while not frontier.empty():
            count += 1
            print 'best: {}'.format(best)
            print 'bestVal: {}'.format(bestVal)
            # take the front element from the frontier
            assignment = frontier.pop()
            # manage frontier and branch-and-bound search
            # prune nodes (and subtrees) as needed
            options = self.expand(assignment)
            for option in options:
                cover = self.eval(nodeNeighbors, option)
                if cover > bestVal:
                    bestVal = cover
                    best = option
                upper_bound = cover + (max_degree * 
                                            (3 - self.num_assignments(option)))
                if upper_bound > bestVal:
                    frontier.pushback(option)

        ### end your code ###

        for i in range(numNodes):
            if (best[i] == 1):
                selected.append(i)

        return selected

    def num_assignments(self, assignment):
        count = 0
        for i in range(len(assignment)):
            if assignment[i] == 1:
                count += 1
        return count

    def expand(self, assignment):
        """
        expand a node in the tree

        returns children of this node in the search tree
        """

        nodes = []

        ### your code goes here  ####
        for i in range(len(assignment)):
            if assignment[i] == 0:
                i_child = list(copy.deepcopy(assignment))
                i_child[i] = 1
                nodes.append(tuple(i_child))
        ### end your code  ###

        return nodes

    def eval(self, nodeNeighbors, x):
        """
        evaluate the value of node x
        nodeNeighbors is an auxiliary data structure
        keeping track of sets of neighbors for each node
        """

        nbrs = Set()
        for i in range(len(x)):
            if x[i] == 1:
                for j in nodeNeighbors[i]:
                    nbrs.add(j)

        return len(nbrs)

    def display(self):
        print "Agent ID ", self.id
        i_child = (i_child[0], 1)

