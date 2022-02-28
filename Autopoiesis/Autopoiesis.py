import random
import numpy as np
np.random.seed(0)
#material_color = {"Water": "Blue", "Phospholipids": "Blue", "Core": "red"}
#material_limit = {"Water": 1, "Phospholipids": 0.9, "Core": 1, }
class Autopoiesis():

    def __init__(self, parameter):
        """

        :param parameter: parameter[0]:initial position x ;  parameter[1]:initial position y ; parameter[2]:initial position y ;
        """
        self.coorx = 0
        self.coory = 0
        self.Boundary = list()
        self.radius = 0
        self.Perimeter = 0
        self.cooling=0
        self.Config(parameter[0], parameter[1], parameter[2])
        self.aveIntegrity=0.15

    def Config(self, coorx, coory, radius):
        """

        :param coorx: initial position x
        :param coory: initial position y
        :param radius: autopoiesis radius
        :return: none
        """
        self.coorx = coorx
        self.coory = coory
        self.Boundary = list()
        self.radius = radius
        for i in range(self.coorx - self.radius, self.coorx + self.radius + 1):
            for j in range(self.coory - self.radius, self.coory + self.radius + 1):
                if 0.9 * self.radius < self._distance((i, j), (self.coorx, self.coory)) < 1.1 * self.radius:
                    self.Boundary.append((i, j))
        self.Perimeter = len(self.Boundary)
        self.lifeTime=0

    def Update(self, rows, cols, Blocks):
        """

        :param rows: size of environment
        :param cols: size of environment
        :param Blocks: Environment
        :return: None
        """
        ## Move the Phospholipids
        self.lifeTime+=1
        self.Draw2Core(rows, cols, Blocks,"Phospholipids")
        # merge the Phospholipids
        self.RandomEnrichment("Phospholipids", Blocks)
        # Phospholipids randomly die
        if random.random() < 0.01:
            self.Dying("Phospholipids", Blocks)
        # Move amino acid
        # random move the core
        if random.random() < 0.005:
            self.MoveCore(rows, cols)
        self.aveIntegrity=(self.aveIntegrity*49+self.Integrity(Blocks))/50
        self.cooling-=1



    def MoveCore(self,rows,cols):
        """
        randomly move the core position
        :return: None
        """
        dx = random.randint(-1,1)
        dy = random.randint(-1,1)
        tempx = self.coorx + dx
        tempy = self.coory + dy
        while not (tempx in range(self.radius+1,rows-self.radius-1) and tempy in range(self.radius+1,cols-self.radius-1)):
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            tempx = self.coorx + dx
            tempy = self.coory + dy
        self.coorx =tempx
        self.coory =tempy
        self.Boundary = list()
        self.Perimeter = 0
        for i in range(self.coorx - self.radius, self.coorx + self.radius + 1):
            for j in range(self.coory - self.radius, self.coory + self.radius + 1):
                if 0.9 * self.radius < self._distance((i, j), (self.coorx, self.coory)) < 1.1 * self.radius:
                    self.Boundary.append((i, j))
        self.Perimeter=len(self.Boundary)

    def Dying(self, material, Blocks):
        """
        material on the edge will die with a rate
        :param material: name of the material
        :param Blocks: Environment
        :return: None
        """
        for item in self.Boundary:
            Blocks[item[0]][item[1]].ions[material] *= 0.99

    def Integrity(self, Blocks):
        """
        Calculates Autopoiesis integrity
        :param Blocks: Environment
        :return: Integrity
        """
        Material = 0
        for item in self.Boundary:
            Material += Blocks[item[0]][item[1]].ions["Phospholipids"]
        return Material / len(self.Boundary)


    def _areaSum(self, row, col, size, Blocks, material):
        """

        :param row: size of the environment
        :param col: size of the environment
        :param size: area size
        :param Blocks: Environment
        :param material: name of the material
        :return: sum of the material
        """
        valuesum = 0
        for i in range(size):
            for j in range(size):
                valuesum += Blocks[row + i][col + j].ions[material]
        return valuesum

    def _ave(self,Blocks, material):
        """
        calculate the sum of material on the edges
        :param Blocks: Environment
        :param material: name of the material
        :return:
        """
        s = 0
        for item in self.Boundary:
            s+=Blocks[item[0]][item[1]].ions[material]
        return s/len(self.Boundary)


    def _distance(self, BlockA, BlockB):
        """

        :param BlockA:
        :param BlockB:
        :return: distance between A and B return double
        """
        return ((BlockA[0] - BlockB[0]) ** 2 + (BlockA[1] - BlockB[1]) ** 2) ** 0.5

    def Draw2Core(self, rows, cols, Blocks,ion):
        """

        :param rows: size of the environment
        :param cols: size of the environment
        :param Blocks: Environment
        :param ion: name of the ion
        :return: None
        """
        coorx1 = np.random.randint(1, rows - 1)
        coory1 = np.random.randint(1, cols - 1)
        coorx2 = coorx1 + np.random.randint(-1, 1)
        coory2 = coory1 + np.random.randint(-1, 1)
        if Blocks[coorx1][coory1].ions[ion] > Blocks[coorx2][coory2].ions[ion]:
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
        """
        edge will randomly enrich certain material,after each enrichment,
        call Equalizer
        :param material: name of material
        :param Blocks: Environment
        :return: None
        """
        effectrange=3
        coorx1,coory1=random.choice(self.Boundary)
        coorx2 = coorx1 + np.random.randint(-effectrange, effectrange)
        coory2 = coory1 + np.random.randint(-effectrange, effectrange)
        attmpts=0
        while (coorx2,coory2) in self.Boundary:
            attmpts+=1
            coorx2 = coorx1 + np.random.randint(-effectrange, effectrange)
            coory2 = coory1 + np.random.randint(-effectrange, effectrange)
            if attmpts>15:
                return
        # Enrichment has upper limit
        try:
            maxiumtake = 1-Blocks[coorx1][coory1].ions[material]
            Blocks[coorx1][coory1].ions[material]+=min(Blocks[coorx2][coory2].ions[material],maxiumtake)
            Blocks[coorx2][coory2].ions[material]=max(Blocks[coorx2][coory2].ions[material]-maxiumtake,0)
            self.Equalizer(material, Blocks[coorx1][coory1], Blocks)
        except:
            pass



    def Equalizer(self, material, Block, Blocks):
        """

        :param material: name of the material
        :param Block: source of the block
        :param Blocks: Environment
        :return: None
        """
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
        """
        Boundary is not stable, it could be moved
        :param rows: size of the environment
        :param cols: size of the environment
        :param Blocks: Environment
        :return:
        """
        coorx1, coory1 = random.choice(self.Boundary)
        coorx2, coory2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
        Blocks[coorx1][coory1], Blocks[coorx2][coory2] = Blocks[coorx2][coory2], Blocks[coorx1][coory1]

    def ChangeSize(self,Grow):
        if Grow and self.radius<6:
            self.radius+=1
        elif self.radius>3:
            self.radius-=1
        self.ChangeSizeTo(self.radius)

    def ChangeSizeTo(self,radius):
        self.radius=radius
        self.Perimeter = 0
        for i in range(self.coorx - self.radius, self.coorx + self.radius + 1):
            for j in range(self.coory - self.radius, self.coory + self.radius + 1):
                if 0.9 * self.radius < self._distance((i, j), (self.coorx, self.coory)) < 1.1 * self.radius:
                    self.Boundary.append((i, j))
                    self.Perimeter += 1



