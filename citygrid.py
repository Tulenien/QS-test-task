from tiletype import *
from random import randint, shuffle
import math
import copy

class CityGrid:
    def __init__(self, rows, cols, obstructionPercentage):
        if (rows < 1 or cols < 1):
            raise ValueError
        self.grid = []
        for i in range(rows):
            temp = []
            for j in range(cols):
                temp.append(TileType.Disconnected)
            self.grid.append(temp)
        self.rows = rows
        self.cols = cols
        self.area = rows * cols
        self.obstructionCount = math.ceil(self.area * 0.01 * 
        obstructionPercentage)
        self.disconnected = self.area - self.obstructionCount
        self.generateObstructions(self.obstructionCount)
        # Generate a copy of grid with obstructions
        self.template = copy.deepcopy(self.grid)

    def generateObstructions(self, count):
        obstructionMap = set()
        while len(obstructionMap) < count:
            row, col = randint(0, self.rows - 1), randint(0, self.cols - 1)
            obstructionMap.add((row, col,))

        for coords in obstructionMap:
            row, col = coords
            self.grid[row][col] = TileType.Obstruction
    
    def resetGrid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = self.template[i][j]

    def positionTowers(self, radius, towers, covered):
        if not (covered < self.disconnected):
            return towers
        else:
            isFirst = False
            if towers == []:
                isFirst = True
            maxVal = 0
            tRow, tCol = 0, 0
            for i in range(self.rows):
                for j in range(self.cols):
                    temp = self.positionEvaluation(i, j, radius, isFirst)
                    if temp > maxVal:
                        maxVal = temp
                        tRow, tCol = i, j
            if maxVal > 0:
                covered += maxVal
                towers.append((tRow, tCol, radius))
                self.placeTower(tRow, tCol, radius)
            else:
                covered = self.disconnected
                return towers
        return self.positionTowers(radius, towers, covered)

    def placeTower(self, row, col, radius):
        startRow = max(row - radius, 0)
        startCol = max(col - radius, 0)
        endRow = min(row + radius + 1, self.rows)
        endCol = min(col + radius + 1, self.cols)
        for i in range(startRow, endRow):
            for j in range(startCol, endCol):
                if self.grid[i][j] == TileType.Disconnected:
                    self.grid[i][j] = TileType.Connected
        self.grid[row][col] = TileType.Tower

    def positionEvaluation(self, row, col, radius, isFirst):
        total = 0
        connectedTowers = 0
        if self.grid[row][col] != TileType.Obstruction and\
           self.grid[row][col] != TileType.Tower:
            startRow = max(row - radius, 0)
            startCol = max(col - radius, 0)
            endRow = min(row + radius + 1, self.rows)
            endCol = min(col + radius + 1, self.cols)
            for i in range(startRow, endRow):
                for j in range(startCol, endCol):
                    currentCell = self.grid[i][j]
                    if currentCell == TileType.Disconnected:
                        total += 1
                    if currentCell == TileType.Connected:
                        connectedTowers += 1
        if not isFirst and connectedTowers < 1:
            total = 0
        return total

    def print_pseudo(self):
        for i in range(self.rows):
            print("\n")
            for j in range(self.cols):
                print(self.grid[i][j].value, end = " ")
        print("\n\n")
