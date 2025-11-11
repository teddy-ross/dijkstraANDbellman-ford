"""
Author(s): Edward Ross, Nick Lagges
This file is an implementation of Bellman-Ford's algorithm.
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



def bellmanFord(numberOfNodes: int, edges: list, source: int) -> tuple:
    """
    Runs Bellman-Ford algorithm given number of nodes, edges, and source node.

    Args:
      numberOfNodes: number of nodes (nodes are assumed 0..numberOfNodes-1)
      edges: list of directed edges as tuples (source, destination, weight)
      source: source node index

    Returns:
      (dist, pred, negCycle)
      - If no negative cycle reachable from source: dist is list of distances, pred is list of predecessors, negCycle is None
      - If a negative cycle reachable from source is found: dist=None, pred=None, negCycle is a list of nodes forming the cycle
    """

    # Initialize
    dist = [float('inf')] * numberOfNodes
    pred = [None] * numberOfNodes
    dist[source] = 0

    # Relax edges up to n-1 times
    for _ in range(numberOfNodes - 1):

        changed = False

        for source, destination, weight in edges:

            if 0 <= source < numberOfNodes and 0 <= destination < numberOfNodes and dist[source] != float('inf'):

                if dist[source] + weight < dist[destination]:

                    dist[destination] = dist[source] + weight
                    pred[destination] = source
                    changed = True

        if not changed:
            break

    # Check for negative-weight cycles reachable from source
    negCycle = None
    for source, destination, weight in edges:
        if 0 <= source < numberOfNodes and 0 <= destination < numberOfNodes and dist[source] != float('inf') and dist[source] + weight < dist[destination]:

            # Found a negative cycle; to extract it, walk predecessors
            x = destination
            # Move n steps to ensure we are inside the cycle
            for _ in range(numberOfNodes):

                if x is None:

                    break

                x = pred[x]

            # If we couldn't find a predecessor chain, treat as no cycle found
            if x is None:

                continue

            # Reconstruct cycle
            cycle = []
            cur = x
            while True:

                cycle.append(cur)
                cur = pred[cur]
                
                if cur is None or cur == x or cur in cycle:
                    break

            # Ensure cycle is in forward order and unique
            if cur is None:
                # failed to reconstruct properly; skip
                continue

            # Close the cycle (ensure starting repeated node not duplicated)
            # cycle currently is [x, pred[x], pred[pred[x]], ...] until it repeats
            cycle.reverse()
            negCycle = cycle

            # Per spec, on detection return None, None, cycle
            dist = None
            pred = None
            break

    return (dist, pred, negCycle)


    



def main() -> int:
    # Read test case and run Bellman-Ford
    numberOfNodes, numberOfEdges, edges, source = getTestCaseInput()
    distances, predecessors, negativeCycle = bellmanFord(numberOfNodes, edges, source)

    
    print("Bellman-Ford:")
    print(distances)
    print(predecessors)
    print(negativeCycle)

    return 0




if __name__ == "__main__":
    main()
