import math
import random

from Block import Block
import matplotlib.pyplot as plt
import numpy as np
import copy

np.random.seed(0)
import seaborn as sns

sns.set()
material_color = {"Water": "Blue", "Phospholipids": "Blue", "Core": "red"}
material_limit = {"Water": 1, "Phospholipids": 0.9, "Core": 1, }
plt.ion()

class Environment():
    def __init__(self, rows, cols, r):

        self.radius = r
        self.Blocks = []
        self.rows = rows
        self.cols = cols
        self.core_location = (rows // 2, cols // 2)
        self.Bounders = list()
        self.Perimeter=0
        for i in range(self.core_location[0]-self.radius,self.core_location[0]+self.radius+1):
            for j in range(self.core_location[1]-self.radius,self.core_location[1]+self.radius+1):
                if 0.9*self.radius<self._distance((i,j),self.core_location)<1.1*self.radius:
                    self.Bounders.append((i,j))
                    self.Perimeter+=1
        self.fig, self.ax1 = plt.subplots(figsize =(12,7))
        data = np.zeros((10, 10))
        h = sns.heatmap(data, ax=self.ax1, cbar=False, cmap="Blues",vmin=0, vmax=1)
        cb = h.figure.colorbar(h.collections[0])
        cb.ax.tick_params(labelsize=18)
        for i in range(rows):
            for j in range(cols):
                self.Blocks.append(Block())
        self.Blocks = np.array(self.Blocks).reshape((cols, rows))
        self.Blocks[rows // 2][cols // 2].core = True
        self.Blocks[rows // 2][cols // 2].ClearMaterial()
        self.Plot("Phospholipids")
        for i in range(500000):
            if i%200==0:
                self.Plot("Phospholipids")
            self.Draw2Core(self.radius)
            self.RandomMove()
            self.RandomEnrichment("Phospholipids")
            if i%500==0:
                self.UnstabelMovement()
                self.Dying("Phospholipids")
            #if i%100==0:
            #    self.Diffution(1,2,"Phospholipids")

        plt.ioff()
        plt.show()

    def Plot(self, item):
        data = []
        for i in range(self.rows):
            for j in range(self.cols):
                data.append(self.Blocks[i][j].ions[item])
        data = np.array(data)
        data = data.reshape((self.cols, self.rows))
        h = sns.heatmap(data, ax=self.ax1, cbar=False, cmap="Blues",vmin=0, vmax=1)
        self.ax1.invert_yaxis()
        Integrity=self.Integrity()
        self.ax1.text(0.5, 0.5, "Autopoiesis Integrity="+str(Integrity), backgroundcolor='white',color="black",alpha=0.5)
        plt.pause(0.00001)

    def Dying(self,material):
        for item in self.Bounders:
            self.Blocks[item[0]][item[1]].ions[material]*=0.99


    def Integrity(self):
        Material=0
        for item in self.Bounders:
            print(self.Blocks[item[0]][item[1]].ions["Phospholipids"],end=" ")
            Material+=self.Blocks[item[0]][item[1]].ions["Phospholipids"]
        return Material/self.Perimeter

    def UnstabelMovement(self):
        coorx1 = np.random.randint(0, self.rows)
        coory1 = np.random.randint(0, self.cols)
        coorx2 = np.random.randint(0, self.rows)
        coory2 = np.random.randint(0, self.cols)
        if abs(self._distance(self.core_location, (coorx1, coory1)) - self.radius) > 0.5 and \
                self.Blocks[coorx1][coory1].ions["Phospholipids"] < 0.8:
            self.Blocks[coorx1][coory1].ions, self.Blocks[coorx2][coory2].ions = self.Blocks[coorx2][coory2].ions, \
                                                                                 self.Blocks[coorx1][coory1].ions

    def RandomMove(self):
        # One block could move around in 8 neighbors
        coorx1 = np.random.randint(1, self.rows - 1)
        coory1 = np.random.randint(1, self.cols - 1)
        coorx2 = coorx1 + np.random.randint(-1, 1)
        coory2 = coory1 + np.random.randint(-1, 1)
        # Core is not movable
        if self.Blocks[coorx1][coory1].core or self.Blocks[coorx2][coory2].core:
            return
        if self.Blocks[coorx1][coory1].ions["Phospholipids"]>0.2 or self.Blocks[coorx2][coory2].ions["Phospholipids"]>0.2:
            return
        # TODO: Add possibility
        self.Blocks[coorx1][coory1].ions, self.Blocks[coorx2][coory2].ions = self.Blocks[coorx2][coory2].ions, \
                                                                             self.Blocks[coorx1][coory1].ions
        pass

    def Diffution(self, Speed, size, material):
        for i in range(0, self.rows - size, size + 1):
            for j in range(0, self.cols - size, size + 1):
                self._ave(i, j, size, material, self._areaSum(i, j, size, material) / (size ** 2))

    def _areaSum(self, row, col, size, material):
        valuesum = 0
        for i in range(size):
            for j in range(size):
                valuesum += self.Blocks[row + i][col + j].ions[material]
        return valuesum

    def _ave(self, row, col, size, material, ave):
        for i in range(size):
            for j in range(size):
                if self.Blocks[row + i][col + j].ions[material] > ave:
                    self.Blocks[row + i][col + j].ions[material] -= ave / 15
                else:
                    self.Blocks[row + i][col + j].ions[material] += ave / 15

    def _distance(self, BlockA, BlockB):
        return ((BlockA[0] - BlockB[0]) ** 2 + (BlockA[1] - BlockB[1]) ** 2) ** 0.5

    def Draw2Core(self, radius):
        coorx1 = np.random.randint(1, self.rows - 1)
        coory1 = np.random.randint(1, self.cols - 1)
        coorx2 = coorx1 + np.random.randint(-1, 1)
        coory2 = coory1 + np.random.randint(-1, 1)
        if self.Blocks[coorx1][coory1].ions["Phospholipids"] > self.Blocks[coorx2][coory2].ions["Phospholipids"]:
            if abs(self._distance((coorx1, coory1), self.core_location) - radius) > abs(
                    self._distance((coorx2, coory2), self.core_location) - radius):
                self.Blocks[coorx1][coory1].ions, self.Blocks[coorx2][coory2].ions = self.Blocks[coorx2][coory2].ions, \
                                                                                     self.Blocks[coorx1][coory1].ions
        else:
            if abs(self._distance((coorx1, coory1), self.core_location) - radius) < abs(
                    self._distance((coorx2, coory2), self.core_location) - radius):
                self.Blocks[coorx1][coory1].ions, self.Blocks[coorx2][coory2].ions = self.Blocks[coorx2][coory2].ions, \
                                                                                     self.Blocks[coorx1][coory1].ions


    def AddMaterial(self, material, quality):
        coorx1 = np.random.randint(0, self.rows)
        coory1 = np.random.randint(0, self.cols)
        if self.Blocks[coorx1][coory1].ions[material] > material_limit[material]:
            return
        self.Blocks[coorx1][coory1].ions[material] += quality

    def Connection(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.Blocks.append(Block())

    def RandomEnrichment(self, material):
        coorx1 = np.random.randint(self.core_location[0]-1.5*self.radius-1, self.core_location[0]+1.5*self.radius+1)
        coory1 = np.random.randint(self.core_location[1]-1.5*self.radius-1, self.core_location[1]+1.5*self.radius+1)
        coorx2 = coorx1 + np.random.randint(-2, 2)
        coory2 = coory1 + np.random.randint(-2, 2)
        # Enrichment has upper limit
        if self._distance((coorx1,coory1),self.core_location)/self.radius<1.5:
            if self.Blocks[coorx1][coory1].ions[material] > self.Blocks[coorx2][coory2].ions[material]:
                self.Blocks[coorx1][coory1].ions[material] += self.Blocks[coorx2][coory2].ions[material]/2
                self.Blocks[coorx2][coory2].ions[material] /= 2
                self.Equalizer(material, (coorx1,coory1))
            else:
                self.Blocks[coorx2][coory2].ions[material] += self.Blocks[coorx1][coory1].ions[material]/2
                self.Blocks[coorx1][coory1].ions[material] /= 2
                self.Equalizer(material, (coorx2,coory2))

    def Equalizer(self,material,coor):
        self.Bounders = sorted(self.Bounders, key=lambda Bounders: self.Blocks[Bounders[0]][Bounders[1]].ions[material])
        for item in self.Bounders:
            if self.Blocks[item[0]][item[1]].ions[material]>0.85:
                break
            self.Blocks[coor[0]][coor[1]].ions[material]-=0.01
            self.Blocks[item[0]][item[1]].ions[material]+=0.01
            if self.Blocks[coor[0]][coor[1]].ions[material]<0.9:
                return


