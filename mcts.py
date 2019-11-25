from copy import deepcopy
from math import sqrt
import math
import random

UCB_CONST = .75

class Node:
    """Node used in MCTS"""
    def __init__(self, state, parent_node):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.parent = parent_node
        self.turn = state.turn
        self.hub = state.hubs[self.turn]
        self.children = {} # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.unexpanded = state.get_moves(self.hub) # Stores unvisited moves to speed up search
        self.visits = 0
        self.value = 0

    def addMove(self, state, move):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move in self.unexpanded:
            self.children[move] = Node(state, self)
            self.unexpanded.remove(move)
            return True
        print('Yikes')
        return False

    def updateValue(self, outcome, root_player):
        """Updates the value estimate for the node's state.
        outcome: +1 for we win, -1 for they win"""
        self.visits += 1
        n = self.visits
        factor = root_player==self.turn
        self.value = self.value * (n-1)/n + factor*outcome/n
        if self.parent is not None:
            self.parent.updateValue(outcome, root_player)

    def UCBWeight(self):
        """Weight from the UCB formula used by parent to select a child.
        This node will be selected by parent with probability proportional
        to its weight."""
        return self.value + sqrt(sqrt(self.parent.visits)/self.visits) * UCB_CONST

    def __lt__(self, other):
        ''' Overrides < so that max works. '''
        return self.UCBWeight() < other.UCBWeight()

def init(board,features,me,hands):
    return mctsAI(board,features,me,hands)

class mctsAI:
    def __init__(self,board,features,me,hands):
        self.name=me
        self.me=me
        #self.features=features
        self.hands=hands
        self.hub=next(iter(hands[me].values())) #initial hub placement because it's OK
        #self.board=board
        self.first_move = True
        
    def move(self, state, rollouts=800):
        """Select a move by Monte Carlo tree search.
        Plays rollouts random games from the root node to a terminal state.
        In each rollout, play proceeds according to UCB while all children have
        been expanded. The first node with unexpanded children has a random child
        expanded. After expansion, play proceeds by selecting uniform random moves.
        Upon reaching a terminal state, values are propagated back along the
        expanded portion of the path. After all rollouts are completed, the move
        generating the highest value child of root is returned.
        Inputs:
            node: the node for which we want to find the optimal move
            state: the state at the root node
            rollouts: the number of root-leaf traversals to run
        Return:
            The legal move from node.state with the highest value estimate
        """
        if self.first_move:
            self.first_move = False
            return self.hub
        root = Node(state, None)
        me = self.name
        for i in range(rollouts):
            if not i%50:
                print(i)
            leaf = self.representative_leaf(root, deepcopy(state)) #deepcopy to not overwrite root state

            value = self.rollout(state)
            leaf.updateValue(-state.get_turn()*value, self.me)
        if root.visits < 1:
            return random_move(root)
        children = root.children
        best_move = max(children, key=lambda move: children[move].visits)
        return best_move

    def representative_leaf(self, node, state):
        ''' Picks a leaf node by descending the tree.
            Creates a new leaf and returns it (and mutates state to be the state at that leaf). '''
        while True:
            children = node.children
            for move in node.unexpanded:
                state.make_move(move, state.turn)
                node.addMove(state, move)
                return children[move]
            if state.is_terminal(self.hands):
                return node
            best_move = max(children, key=children.values())
            state.make_move(best_move, state.turn)
            node = children[best_move]
    
    def rollout(self, state):
        ''' Returns the value of a random rollout from a node.'''
        i = 0
        while not state.is_terminal(self.hands):
            moves = state.get_moves(self.hub)
            #print(len(moves), i, state.value(self.hands))
            i +=1
            state.make_move(random.sample(moves, 1)[0], state.turn)
        return (state.value(self.hands) == state.turn)*2 -1
