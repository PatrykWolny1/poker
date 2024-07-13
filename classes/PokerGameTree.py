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



