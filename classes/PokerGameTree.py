import numpy as np
from scipy.special import binom
from abc import abstractmethod

class ComputeObject(object):
    
    def __init__(self, name: str = '', threshold: float = 0, result_var: float = 0, data = None):
        self.name = name
        self.data = data
        self.threshold = threshold
        self.result_var = result_var
    
    @abstractmethod
    def computing(self):
        pass
    
    @abstractmethod
    def result(self):
        pass

class ThreeCardsProbability(ComputeObject):
    
    def __init__(self, name: str = '', threshold: float = 0, result_var: float = 0, data = None):
        super().__init__(name, threshold, result_var, data)
        
    def computing(self):
        count_1 = 0
        
        for idx in range(0, len(self.data)):
            if self.data[idx] < self.threshold:
                self.data[idx] = None
                count_1 += 1
        
        self.result_var = [count_1/len(self.data), 1 - (count_1/len(self.data))]  
          
    def result(self):
        return self.result_var
    
class ThreeCardsSum(ComputeObject):
    
    def __init__(self, name: str = '', threshold: float = 0, result_var: float = 0, data = None):
        super().__init__(name, threshold, result_var, data)
        
    def computing(self):
        sum = 0
        
        for idx in range(0, len(self.data)):
            sum += self.data[idx]
            
        if sum >= 24:
            self.result_var = 0.1
        else:
            self.result_var = 0
            
    def result(self):
        return self.result_var

class ArrangementProbability(ComputeObject):
    
    def __init__(self, name: str = '', threshold: float = 0, result_var: float = 0, data = None):
        super().__init__(name, threshold, result_var, data)
        
    def computing(self):
        sum = 0
        
        for idx in range(0, len(self.data)):
            sum += self.data[idx]
            
        if sum >= 24:
            self.result_var = 0.1
        else:
            self.result_var = 0
            
    def result(self):
        return self.result_var


class Node(object):
    
    def __init__(self, name: str):
        self.name = name
        
        self.branches = []
        self.internal_nodes = []
        self.leaf_nodes = []
            
    def __str__(self):
        str_result = '\t\t\t' + self.name
        
        str_result += '\n\n'

        logic_more = False
        logic_less = False
        
        for idx in range(0, len(self.branches)):
            str_result += '\t\t' + str(self.branches[idx])
            for idx1 in range(0, len(self.branches)):
                if self.branches[idx].threshold > self.branches[idx1].threshold and logic_more == False:
                    str_result_1 = '\t\t\t\t  ' + str(self.leaf_nodes[self.leaf_nodes.index([x for x in self.leaf_nodes if x.result == True][0])])
                    logic_more = True
                    
                elif logic_less == False:
                    str_result_2 = '\t   ' + str(self.leaf_nodes[self.leaf_nodes.index([x for x in self.leaf_nodes if x.result == False][0])])
                    logic_less = True
        
        str_result += '\n'
        str_result += str_result_2 + str_result_1
           
        str_result += '\n' 
        
        return str_result
        
class InternalNode(object):

    def __init__(self, name: str, branches = None, leaf_nodes = None):
        self.name = name
        self.branches = branches
        self.leaf_nodes = leaf_nodes
        
    def __str__(self) -> str:
        return self.name
        
class Branch(object):
    
    def __init__(self, name: str, threshold: float, computeobject: ComputeObject):
        self.name = name
        self.threshold = threshold  
    
    def __str__(self):
        return self.name + "(" + str(self.threshold) + ")"    
          
class LeafNode(object):
    
    def __init__(self, name: str, result = None):
        self.name = name
        self.result = result
        
    def __str__(self):
        return self.name


cards = [1, 2, 3, 4, 5]

root = Node("ONE PAIR")

internal_nodes = [InternalNode("Exchange Cards?")]



computeobject = ThreeCardsSum("Three Cards Sum", cards, 24)

for i in range(0, 2):
    branches = [Branch(i + 1, computeobject.result())]

root.branches = branches

leaf_nodes = [LeafNode("Yes", True), LeafNode("No", False)]
root.leaf_nodes = leaf_nodes

computeobject = ThreeCardsProbability("Three Cards Probability", cards, 8)
computeobject.computing()

for i in range(0, 2):
    branches = [Branch(i + 1, computeobject.result()[i])]

root.branches = branches

leaf_nodes = [LeafNode("Two Cards", 1), LeafNode("Three Cards", 2)]

internal_nodes = [InternalNode(root.leaf_nodes[root.leaf_nodes.index([x for x in root.leaf_nodes if x.result == True][0])]).name, 
                  branches, leaf_nodes]



print(root)


