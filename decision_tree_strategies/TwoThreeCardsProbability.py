import ComputeObject

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
