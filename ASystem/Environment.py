from Autopoiesis import Autopoiesis
from Block import Block
import numpy as np

material_limit = {"Water": 1, "Phospholipids": 0.9, "Core": 1, }


class Environment():
    def __init__(self, ionsLimit, rows, cols, autopoiesis, division=False):

        """
        
        :param rows: Environment Size y
        :param cols: Environment Size x
        :param r: Normal ASystem Size
        """

        # Create environment
        self.Blocks = []
        self.rows = rows
        self.cols = cols
        self.timestep = 1
        self.division = division
        for i in range(rows):
            for j in range(cols):
                self.Blocks.append(Block(ionsLimit))
        self.Blocks = np.array(self.Blocks).reshape((cols, rows))

        # self.Plot("Phospholipids")
        # Create AutopoiesisList
        self.AutopoiesisList = []
        self.AutopoiesisID=1
        for item in autopoiesis:
            self.AutopoiesisList.append(Autopoiesis(item, self.AutopoiesisID))
            self.AutopoiesisID+=1

    def Update(self):
        """
        Environment Update
        :return: None
        """
        self.timestep += 1
        for i in range(10):
            self.RandomMove()
            for A in self.AutopoiesisList:
                try:
                    A.cooling -= 1
                    A.Update(self.rows, self.cols, self.Blocks)
                    if A.aveIntegrity > 0.8 and A.cooling < 1:
                        A.ChangeSize(True)
                        A.cooling = 2500
                    elif self.timestep > 500 and A.aveIntegrity < 0.35 and A.cooling < 1:
                        A.ChangeSize(False)
                        A.cooling = 2500
                    #
                    if A.radius > 4 and self.division:
                        x = A.coorx + round(15 * np.random.rand() - 7)
                        y = A.coory + round(15 * np.random.rand() - 7)
                        r = 3
                        A.ChangeSizeTo(3)
                        self.MoveAway(A)
                        self.AutopoiesisList.append(Autopoiesis((x, y, r), self.AutopoiesisID))
                        return
                    if A.radius == 3 and A.aveIntegrity < 0.25 and A.lifeTime > 2000:
                        self.AutopoiesisList.remove(A)
                except:
                    return

            # if i%100==0:
            #    self.Diffution(1, 2, "Phospholipids")

    def RandomMove(self):
        """
        Partial could randomly move
        :return:
        """
        # One block could move around in 8 neighbors
        for _ in range(20):
            coorx1 = np.random.randint(1, self.rows - 1)
            coory1 = np.random.randint(1, self.cols - 1)
            coorx2 = coorx1 + np.random.randint(-1, 1)
            coory2 = coory1 + np.random.randint(-1, 1)
            # Core is not movable
            if self.Blocks[coorx1][coory1].core or self.Blocks[coorx2][coory2].core:
                continue
            if self.Blocks[coorx1][coory1].ions["Phospholipids"] > 0.2 or self.Blocks[coorx2][coory2].ions[
                "Phospholipids"] > 0.2:
                continue
            # TODO: Add possibility
            self.Blocks[coorx1][coory1].ions, self.Blocks[coorx2][coory2].ions = self.Blocks[coorx2][coory2].ions,self.Blocks[coorx1][coory1].ions


    def Plot(self, item):
        data = []
        for i in range(self.rows):
            for j in range(self.cols):
                data.append(self.Blocks[i][j].ions[item])
        data = np.array(data)
        data = data.reshape((self.cols, self.rows))
        return data

    def _areaSum(self, row, col, size, material):
        """

        :param row: start point row
        :param col: start point col
        :param size: area size
        :param material: material
        :return: Sum of the area
        Example:
        _areaSum(1, 1, 2, material)
        return (1,1)+(1,2)+(2,1)+(2,2)
        """
        valuesum = 0
        for i in range(size):
            for j in range(size):
                valuesum += self.Blocks[row + i][col + j].ions[material]
        return valuesum

    def _distance(self, BlockA, BlockB):
        """
        calculate distance between two blocks
        :param BlockA:
        :param BlockB:
        :return:
        """
        return ((BlockA[0] - BlockB[0]) ** 2 + (BlockA[1] - BlockB[1]) ** 2) ** 0.5

    def AddMaterial(self, material, quality):
        """

        :param material: name of the material
        :param quality:
        :return: None
        """
        coorx1 = np.random.randint(0, self.rows)
        coory1 = np.random.randint(0, self.cols)
        if self.Blocks[coorx1][coory1].ions[material] > material_limit[material]:
            return
        self.Blocks[coorx1][coory1].ions[material] += quality

    def MoveAway(self, A):
        if len(self.AutopoiesisList) == 1:
            return
        closestA, distance = self.FindClosest(A)
        if distance > A.radius:
            return
        else:
            print(closestA,distance)

    def FindClosest(self, A):
        """
        FindClosest ASystem to the A
        :param A: An autopoiesis
        :return: id of the Closest one, distance
        """
        closest = None
        closestdistance = np.inf
        for ID in range(len(self.AutopoiesisList)):
            if self.AutopoiesisList[ID] == A:
                continue
            if self._distance(self.AutopoiesisList[ID], A) < closestdistance:
                closest = ID
                closestdistance = self._distance(self.AutopoiesisList[ID], A)
        return closest, closestdistance
