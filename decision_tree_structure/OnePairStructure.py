from decision_tree_structure import Node, InternalNode, Branch, LeafNode
from decision_tree_strategies import ComputeObject
from decision_tree_strategies import OnePairProbability
from decision_tree_strategies import ThreeCardsProbability
from decision_tree_strategies import TwoThreeCardsProbability 

cards = [1, 1, 12, 6, 5]

# Probability of exchaning cards rises when high card value is less than x

cards_rest = [13, 6, 5]

root = Node("ONE PAIR")

nk = [[13, 1], [4, 2], [47, 2]]

print(cards)


computeobject_1 = OnePairProbability("One Pair Probability", data=cards_rest.copy(), nk=nk)
computeobject_1.computing()

computeobject_2 = ThreeCardsProbability("Three Cards Probability", data=cards_rest.copy(), threshold=8, p1=0.128)
computeobject_2.computing()

computeobject = [ComputeObject(result_var=(computeobject_1 + computeobject_2)), ComputeObject(result_var=(1 - (computeobject_1 + computeobject_2)))]

#result_exchange_cards = [computeobject_1 + computeobject_2, 1 - (computeobject_1 + computeobject_2)]

branches = []

for i in range(0, 2):
    branches.append(Branch(str(i + 1), computeobject[i].result()))
leaf_nodes = [LeafNode("No", False)]

internal_nodes = [InternalNode("Exchange Cards?", branches, leaf_nodes)]
root.internal_nodes.append(internal_nodes)

computeobject = TwoThreeCardsProbability("Two/Three Cards Probability", threshold=8, data=cards_rest.copy())
computeobject.computing()

branches = []

for i in range(0, 2):
    branches.append(Branch(str(i + 1), computeobject.result()[i]))

leaf_nodes = [LeafNode("Two Cards", 1), LeafNode("Three Cards", 2)]

internal_nodes = [InternalNode("Yes", branches, leaf_nodes)]
root.internal_nodes.append(internal_nodes)

# root.branches = branches

# leaf_nodes = [LeafNode("Two Cards", 1), LeafNode("Three Cards", 2)]

# internal_nodes = [InternalNode(root.leaf_nodes[root.leaf_nodes.index([x for x in root.leaf_nodes if x.result == True][0])]).name, 
#                   branches, leaf_nodes]

print(root)

