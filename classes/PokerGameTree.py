import numpy as np
from scipy.special import binom
from abc import abstractmethod

class ComputeObject(object):
    
    def __init__(self, name: str = '', result_var: float = 0, data = None):
        self.name = name
        self.data = data
        self.result_var = result_var
    
    @abstractmethod
    def computing(self):
        pass
    
    @abstractmethod
    def result(self):
        return self.result_var
    
    def __add__(self, other):
        return self.result_var + other.result_var

class TwoThreeCardsProbability(ComputeObject):
    
    def __init__(self, name: str = '', threshold: float = 0, result_var: float = 0, data = None):
        super().__init__(name, result_var, data)
        self.threshold = threshold
    def computing(self):
        count_1 = 0

        for idx in range(0, len(self.data)):
            if self.data[idx] < self.threshold:
                self.data[idx] = None
                count_1 += 1
        
        self.result_var = [count_1/len(self.data), 1 - (count_1/len(self.data))]  
          
    def result(self):
        return self.result_var
    
class ThreeCardsProbability(ComputeObject):
    
    def __init__(self, name: str = '', result_var: float = 0, data = None, threshold: int = 0, p1: float = 0.01):
        super().__init__(name, result_var, data)
        self.threshold = threshold
        self.p1 = p1
        
    def computing(self):
        if max(self.data) > self.threshold:
            self.result_var = self.p1
            
    def result(self):
        return self.result_var
        
class OnePairProbability(ComputeObject):
    
    def __init__(self, name: str = '', result_var: float = 0, data = None, nk: int = None):
        super().__init__(name, result_var, data)
        self.nk = nk
        
    def computing(self):
        binom_list = []

        for idx in range(0, len(self.nk)):
            binom_list.append(binom(self.nk[idx][0], self.nk[idx][1]))
        
        Px = (binom_list[0] * binom_list[1]) / binom_list[2]
                
        self.result_var = Px  
        
    def result(self):
        return self.result_var

class Node(object):
    
    def __init__(self, name: str):
        self.name = name
        
        self.branches = []
        self.internal_nodes = []
        self.leaf_nodes = []
            
    def __str__(self):
        
        # ROOT
        str_result = '\t\t\t\t\t' + self.name
        
        str_result += '\n\n'
        
        # ExchangeCards?
        str_result += '\t\t\t\t    ' + str(self.internal_nodes[0][0])

        str_result += '\n\n'
        
        # Branches p(x) 1   p(x) 2 
        for idx in range(0, len(self.internal_nodes[0][0].branches)):
            str_result += '\t\t\t' + str(self.internal_nodes[0][0].branches[idx])
        
        str_result += '\n'
        
        # No 
        str_result += '\t\t\t  ' + str(self.internal_nodes[0][0].leaf_nodes[0])
        
        # Yes
        str_result += '\t\t\t\t   ' + str(self.internal_nodes[1][0])
        
        str_result += '\n'
        
        str_result += '\t\t\t\t\t' + str(self.internal_nodes[1][0].branches[0])
        
        str_result += '\t\t\t' + str(self.internal_nodes[1][0].branches[1])
        
        str_result += '\n'
        
        str_result += '\t\t\t\t\t' + str(self.internal_nodes[1][0].leaf_nodes[0])
        str_result += '\t\t\t' + str(self.internal_nodes[1][0].leaf_nodes[1])
        
        
        str_result 
     
        return str_result
            
class InternalNode(object):

    def __init__(self, name: str, branches = None, leaf_nodes = None):
        self.name = name
        self.branches = branches
        self.leaf_nodes = leaf_nodes
        
    def __str__(self) -> str:
        return self.name
        
class Branch(object):
    
    def __init__(self, name: str = '', threshold: float = 0):
        self.name = name
        self.threshold = threshold  
    
    def __str__(self):
        return self.name + "(" + str("{:.4f}".format(self.threshold)) + ")"    
          
class LeafNode(object):
    
    def __init__(self, name: str, result = None):
        self.name = name
        self.result = result
        
    def __str__(self):
        return self.name


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


