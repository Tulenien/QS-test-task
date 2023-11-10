import math
import heapq
class Graph:
    def __init__(self, connections):
        self.nodes = {}

    def addNode(self, node):
        if not node in self.nodes:
            self.nodes[node] = {'neighbors': []}

    def addEdge(self, node1, node2):
        # Adding an edge between two nodes
        if not node2 in self.nodes[node1]['neighbors']:
            self.nodes[node1]['neighbors'].append(node2)
        if not node1 in self.nodes[node2]['neighbors']:
            self.nodes[node2]['neighbors'].append(node1)

    def calculatePotential(self, x0, y0, x1, y1):
        diff1 = x1 - x0
        diff2 = y1 - y0
        return math.sqrt(diff1 * diff1 + diff2 * diff2)

    def dijkstra(self, towers, start, end):
        paths = {node: [] for node in self.nodes}
        distances = {node: math.inf for node in self.nodes}
        distances[start] = 0
        priorityQ = [(0, start)]

        while priorityQ:
            currentDistance, currentNode = heapq.heappop(priorityQ)

            if currentDistance > distances[currentNode]:
                continue

            if currentNode == end:
                return paths[end]

            for neighbor in self.nodes[currentNode]['neighbors']:
                distance = currentDistance + self.calculatePotential(towers[start].x, towers[start].y, 
                towers[neighbor].x, towers[neighbor].y)

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    paths[neighbor] = paths[currentNode] + [currentNode]
                    heapq.heappush(priorityQ, (distance, neighbor))
        return math.inf
