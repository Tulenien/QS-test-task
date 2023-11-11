from citygrid import *
from graph import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    cityGrid = CityGrid(10, 10, 30)
    towers = cityGrid.positionTowers(1)
    towers = cityGrid.mapTowerConnections(towers)
    connections = cityGrid.setOfConnections(towers)

    # Create a graph
    g = Graph(connections)

    for connection in connections:
        node1, node2 = connection
        g.addNode(node1)
        g.addNode(node2)
        g.addEdge(node1, node2)

    connectionPaths = []
    for i in range(len(towers) - 1):
        for j in range(i + 1, len(towers)):
            path = g.dijkstra(towers, i, j) + [j]
            connectionPaths.append(path)

    cityGrid.plot(towers, connectionPaths)