
import numpy as np
Material = {"Water": "Blue", "Phospholipids": "Yellow"}
class Block():
    def __init__(self):
        self.core = False
        self.type = None
        self.ions={"Water":0.99,"Phospholipids":np.random.rand()/10}
        self.status=np.random.rand()
        self.connection = False
    def PrintSelf(self):
        pass
    def ClearMaterial(self):
        for item in self.ions:
            self.ions[item]=0

