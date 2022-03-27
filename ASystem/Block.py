import numpy as np

class Block():
    def __init__(self,ionsLimit):
        self.core = False
        self.type = None
        self.ions={key:value*np.random.rand() for key,value in ionsLimit.items()}
        self.status=np.random.rand()
        self.connection = False
    def PrintSelf(self):
        pass
    def ClearMaterial(self):
        for item in self.ions:
            self.ions[item]=0

