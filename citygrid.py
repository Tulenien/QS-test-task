from tiletype import *
from tower import *
from random import randint, shuffle
import math
import copy

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CityGrid:
    def __init__(self, rows, cols, obstructionPercentage):
        if (rows < 1 or cols < 1 or 100 < obstructionPercentage < 0):
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

    def positionTowers(self, radius):
        covered = 0
        towers = []
        isFirst = True
        while covered < self.disconnected:
            maxVal = 0
            tRow, tCol = 0, 0
            for i in range(self.rows):
                for j in range(self.cols):
                    temp = self.positionEvaluation(i, j, radius, isFirst)
                    if temp > maxVal:
                        maxVal = temp
                        tRow, tCol = i, j
            isFirst = False
            if maxVal > 0:
                covered += maxVal
                towers.append((tRow, tCol, radius))
                self.placeTower(tRow, tCol, radius)
            else:
                break
        return towers

    def positionTowersRecursive(self, radius, towers, covered):
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
                    if currentCell == TileType.Tower:
                        connectedTowers += 1
        if not isFirst and connectedTowers < 1:
            total = 0
        return total

    def mapTowerConnections(self, towers):
        towersMap = copy.deepcopy(self.template)
        result = []
        for tower in towers:
            row, col, radius = tower
            temp = Tower(radius, (row, col))
            result.append(temp)
            startRow = max(row - radius, 0)
            startCol = max(col - radius, 0)
            endRow = min(row + radius + 1, self.rows)
            endCol = min(col + radius + 1, self.cols)
            for i in range(startRow, endRow):
                for j in range(startCol, endCol):
                    if type(towersMap[i][j]) == Tower:
                        towersMap[i][j].connect(temp)
                        temp.connect(towersMap[i][j])
            towersMap[row][col] = temp
        return result

    def setOfConnections(self, towers):
        pairs = set()
        for i in range(len(towers)):
            for connection in towers[i].connections:
                pairs.add((i, towers.index(connection)))
        return pairs

    def print_pseudo(self):
        for i in range(self.rows):
            print("\n")
            for j in range(self.cols):
                print(self.grid[i][j].value, end = " ")
        print("\n\n")

    def plot(self, towers):
        obstructionColor = 0
        towerColor = 10
        connectedColor = 20
        disconnectedColor = 40
        heatmap = np.arange(self.area).reshape(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                value = self.grid[i][j]
                if value == TileType.Obstruction:
                    heatmap[i][j] = obstructionColor
                elif value == TileType.Tower:
                    heatmap[i][j] = towerColor
                elif value == TileType.Connected:
                    heatmap[i][j] = connectedColor
                elif value == TileType.Disconnected:
                    heatmap[i][j] = disconnectedColor
        delta = (disconnectedColor - connectedColor - 5) / len(towers)
        for tower in towers:
            row, col, radius = tower
            startRow = max(row - radius, 0)
            startCol = max(col - radius, 0)
            endRow = min(row + radius + 1, self.rows)
            endCol = min(col + radius + 1, self.cols)
            for i in range(startRow, endRow):
                for j in range(startCol, endCol):
                    if self.grid[i][j] == TileType.Connected:
                        heatmap[i][j] += delta
        annotLabels = np.empty_like(heatmap, dtype=str)
        annotMaskTower = heatmap == towerColor
        annotMaskDisconnected = heatmap == disconnectedColor
        annotLabels[annotMaskTower] = 'T'
        annotLabels[annotMaskDisconnected] = 'D'
        ax = sns.heatmap(heatmap, annot=annotLabels, fmt='', linewidth=0.1)
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticks([obstructionColor, towerColor, connectedColor, disconnectedColor])
        colorbar.set_ticklabels(["Obstruction", "(T)ower", "Connection", "(D)isconnected"])
        plt.show()
