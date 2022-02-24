import random
import numpy as np
np.random.seed(0)
#material_color = {"Water": "Blue", "Phospholipids": "Blue", "Core": "red"}
#material_limit = {"Water": 1, "Phospholipids": 0.9, "Core": 1, }
class Autopoiesis():

    def __init__(self, parameter):
        self.coorx = 0
        self.coory = 0
        self.Boundary = list()
        self.radius = 0
        self.Perimeter = 0
        self.Config(parameter[0], parameter[1], parameter[2])

    def Config(self, coorx, coory, radius):
        self.coorx = coorx
        self.coory = coory
        self.Boundary = list()
        self.radius = radius
        self.Perimeter = 0
        for i in range(self.coorx - self.radius, self.coorx + self.radius + 1):
            for j in range(self.coory - self.radius, self.coory + self.radius + 1):
                if 0.9 * self.radius < self._distance((i, j), (self.coorx, self.coory)) < 1.1 * self.radius:
                    self.Boundary.append((i, j))
                    self.Perimeter += 1

    def Update(self, rows, cols, Blocks):
        self.Draw2Core(rows, cols, Blocks)
        self.RandomEnrichment("Phospholipids", Blocks)
        if random.random() < 0.01:
            self.Dying("Phospholipids", Blocks)
        if random.random() < 0.0025:
            self.MoveCore()


    def MoveCore(self):
        dx = random.randint(-1,1)
        dy = random.randint(-1,1)
        self.coorx +=dx
        self.coory +=dy
        self.Boundary = list()
        self.Perimeter = 0
        for i in range(self.coorx - self.radius, self.coorx + self.radius + 1):
            for j in range(self.coory - self.radius, self.coory + self.radius + 1):
                if 0.9 * self.radius < self._distance((i, j), (self.coorx, self.coory)) < 1.1 * self.radius:
                    self.Boundary.append((i, j))
                    self.Perimeter += 1

    def Dying(self, material, Blocks):
        for item in self.Boundary:
            Blocks[item[0]][item[1]].ions[material] *= 0.99

    def Integrity(self, Blocks):
        Material = 0
        for item in self.Boundary:
            Material += Blocks[item[0]][item[1]].ions["Phospholipids"]
        return Material / self.Perimeter

    def _areaSum(self, row, col, size, Blocks, material):
        valuesum = 0
        for i in range(size):
            for j in range(size):
                valuesum += Blocks[row + i][col + j].ions[material]
        return valuesum

    def _ave(self,Blocks, material):
        s = 0
        for item in self.Boundary:
            s+=Blocks[item[0]][item[1]].ions[material]
        return s/len(self.Boundary)


    def _distance(self, BlockA, BlockB):
        return ((BlockA[0] - BlockB[0]) ** 2 + (BlockA[1] - BlockB[1]) ** 2) ** 0.5

    def Draw2Core(self, rows, cols, Blocks):
        coorx1 = np.random.randint(1, rows - 1)
        coory1 = np.random.randint(1, cols - 1)
        coorx2 = coorx1 + np.random.randint(-1, 1)
        coory2 = coory1 + np.random.randint(-1, 1)
        if Blocks[coorx1][coory1].ions["Phospholipids"] > Blocks[coorx2][coory2].ions["Phospholipids"]:
            if abs(self._distance((coorx1, coory1), (self.coorx, self.coory)) - self.radius) > abs(
                    self._distance((coorx2, coory2), (self.coorx, self.coory)) - self.radius):
                Blocks[coorx1][coory1].ions, Blocks[coorx2][coory2].ions = Blocks[coorx2][coory2].ions, \
                                                                           Blocks[coorx1][coory1].ions
        else:
            if abs(self._distance((coorx1, coory1), (self.coorx, self.coory)) - self.radius) < abs(
                    self._distance((coorx2, coory2), (self.coorx, self.coory)) - self.radius):
                Blocks[coorx1][coory1].ions, Blocks[coorx2][coory2].ions = Blocks[coorx2][coory2].ions, \
                                                                           Blocks[coorx1][coory1].ions

    def RandomEnrichment(self, material, Blocks):
        effectrange=3
        coorx1,coory1=random.choice(self.Boundary)
        coorx2 = coorx1 + np.random.randint(-effectrange, effectrange)
        coory2 = coory1 + np.random.randint(-effectrange, effectrange)
        while (coorx2,coory2) in self.Boundary:
            coorx2 = coorx1 + np.random.randint(-effectrange, effectrange)
            coory2 = coory1 + np.random.randint(-effectrange, effectrange)
        # Enrichment has upper limit
        maxiumtake = 1-Blocks[coorx1][coory1].ions[material]
        Blocks[coorx1][coory1].ions[material]+=min(Blocks[coorx2][coory2].ions[material],maxiumtake)
        Blocks[coorx2][coory2].ions[material]=max(Blocks[coorx2][coory2].ions[material]-maxiumtake,0)
        self.Equalizer(material, Blocks[coorx1][coory1], Blocks)



    def Equalizer(self, material, Block, Blocks):
        random.shuffle(self.Boundary)
        ave = self._ave(Blocks,material)
        for item in self.Boundary:
            if Block.ions[material] < 0.7:
                return
            if Blocks[item[0]][item[1]].ions[material] > ave:
                continue
            else:
                Block.ions[material] -= 0.05
                Blocks[item[0]][item[1]].ions[material] += 0.05




    def UnstabelMovement(self, rows, cols, Blocks):
        coorx1, coory1 = random.choice(self.Boundary)
        coorx2, coory2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
        Blocks[coorx1][coory1], Blocks[coorx2][coory2] = Blocks[coorx2][coory2], Blocks[coorx1][coory1]


