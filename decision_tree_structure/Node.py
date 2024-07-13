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
