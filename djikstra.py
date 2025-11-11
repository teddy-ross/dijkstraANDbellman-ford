import heapq
from collections import defaultdict
"""
Author(s): Edward Ross, Nick Lagges
This file is an implementation of Djikstra's algorithm.
"""


def getTestCaseInput() -> list:

    """
    Gets the test case inputs from a txt file

    Args:
    None

    Returns:
    list [numberOfNodes, numberOfEdges, edges = (src, dest, weight), source node]
    """

    print("Enter test case file name")
    inputFile = input()

    with open(inputFile, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # First line: numberOfNodes (nodes), numberOfEdges (edges)
    numberOfNodes, numberOfEdges = map(int, lines[0].split())

    # Next m lines: edges (source, destination, weight)
    edges = []

    for line in lines[1:numberOfEdges+1]:
        
        source, destination, weight = map(int, line.split())
        edges.append((source, destination, weight))

    # Last line: source node
    source = int(lines[numberOfEdges+1])
    
    return [numberOfNodes, numberOfEdges, edges, source]

"""
Runs Dijkstra's Algorithm Given n node, m edges, and source node

Args: 
    None
Returns:
    tuple: (distances from source to each node, predecessors)
"""
def dijkstra() -> tuple:
    #Get user input 
    numberOfNodes, numberOfEdges, edges, sourceNode = getTestCaseInput()
    
    #Build adjacency list
    graph = defaultdict(list)
    for source, destination, weight in edges:
        graph[source].append((destination, weight))

    #Intialize a minHeap (to process shortest distance first) with a tuple (time to reach node, node) and a dictionary to keep track of the current shortest distance from source -> node
    # distances: best known distances (tentative then final)
    dist = [float('inf')] * numberOfNodes
    dist[sourceNode] = 0

    #Intialize a list to keep track of predecessor nodes.
    predecessors = [None] * numberOfNodes

    #We intialize a minheap of (dist, node) to make sure we process shortest distances first, as well as a visited dictionary to keep track of which nodes have been finalized (visited) (O(1) lookup time)
    minHeap = [(0, sourceNode)]

    #node : shortest distance from source to node
    visited = {}

    while minHeap:
        distance, node = heapq.heappop(minHeap)

        # If the node has already been visited (finalized), skip it.
        # Use dict.get to avoid KeyError for nodes not yet seen in the dict.
        if visited.get(node):
            continue

        visited[node] = True

        # If the popped distance is larger than the recorded best, skip
        if distance > dist[node]:
            continue

        for destination, weight in graph[node]:
            if destination < 0 or destination >= numberOfNodes:
                continue
            new_dist = distance + weight
            # If we found a better path, update and push to heap
            if new_dist < dist[destination]:
                dist[destination] = new_dist
                predecessors[destination] = node
                heapq.heappush(minHeap, (new_dist, destination))

    return (dist, predecessors)


def main() -> int:
    distances, predecessors = dijkstra()

    # Any distance equal to float('inf') is unreachable
    distanceList = [d if d != float('inf') else float('inf') for d in distances]

    # Output
    print("Dijkstra:")
    print("dist:", distanceList)
    print("pred:", predecessors)

    return 0
    
if __name__ == "__main__":

    main()
