from decision_tree_structure.Node import Node
from decision_tree_structure.InternalNode import InternalNode
from decision_tree_structure.Branch import Branch
from decision_tree_structure.LeafNode import LeafNode
from decision_tree_strategies.ComputeObject import ComputeObject
from decision_tree_strategies.OnePairProbability import OnePairProbability
from decision_tree_strategies.ThreeCardsProbability import ThreeCardsProbability 
from decision_tree_strategies.TwoThreeCardsProbability import TwoThreeCardsProbability 

class OnePairStructureStrategy(object):
    def __init__(self, cards: list = None):
        self.cards = cards

        # Probability of exchaning cards rises when high card value is less than x

        self.cards_rest = self.cards[2:6]

        self.root = Node("ONE PAIR")

        self.nk = [[13, 1], [4, 2], [47, 2]]

        print(self.cards)
        
        computeobject_1 = OnePairProbability("One Pair Probability", data=self.cards_rest.copy(), nk=self.nk)
        computeobject_1.computing()

        computeobject_2 = ThreeCardsProbability("Three Cards Probability", data=self.cards_rest.copy(), threshold=8, p1=0.128)
        computeobject_2.computing()

        computeobject = [ComputeObject(result_var=(computeobject_1 + computeobject_2)), ComputeObject(result_var=(1 - (computeobject_1 + computeobject_2)))]

        branches = []

        for i in range(0, 2):
            branches.append(Branch(str(i + 1), computeobject[i].result()))
        leaf_nodes = [LeafNode("No", False)]

        internal_nodes = [InternalNode("Exchange Cards?", branches, leaf_nodes)]
        self.root.internal_nodes.append(internal_nodes)

        computeobject = TwoThreeCardsProbability("Two/Three Cards Probability", threshold=8, data=self.cards_rest.copy(), p1=0.2)
        computeobject.computing()

        branches = []

        for i in range(0, 2):
            branches.append(Branch(str(i + 1), computeobject.result()[i]))

        leaf_nodes = [LeafNode("Two Cards", 1), LeafNode("Three Cards", 2)]

        internal_nodes = [InternalNode("Yes", branches, leaf_nodes)]
        self.root.internal_nodes.append(internal_nodes)

        print(self.root)
