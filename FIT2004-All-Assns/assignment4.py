"""
Assignment 4 file for FIT2004 by Ian Tongs, 2020. Contains all required functions.
When run, produces no independent outputs as is. All complexities are optimal.

@author         Ian Tongs, 27765369
@since          30 May 2020
"""

# Imports:
import sys      # Not used. Should delete this import.
import heapq    # It is mentioned in the forums we can import heapq for use without losing marks to implement a heap for
                # our dijkstra's algorithm.


# Functions:

########################################################################################################################
# Tasks 1-3
########################################################################################################################

class Graph:
    """
    Class for graph implementation
    """

    def __init__(self, gfile):
        """
        Initialises a graph (and an augmented graph for Q3) by importing the edges from a text file

        @param self         The graph we are initialising
        @param gfile        The name of the file we are importing the data from
        @complexity         Auxiliary Space: O(V^2) where V is the number of vertices in the graph
                            Time: O(V^2) where V is the number of vertices in the graph
        """
        file = open(gfile, "r")                     # Open the file

        line_checker = 0

        for line in file:

            if line_checker == 0:
                # Initialise graph
                self.Graph = [[None for _ in range(int(line))] for _ in range(int(line))]

                # Initialise the graph for Q 3:
                self.iceGraph = [[None for _ in range(3 * int(line))] for _ in range(3 * int(line))]

            else:
                # Split line and set values
                line_list = line.split()
                self.Graph[int(line_list[0])][int(line_list[1])] = int(line_list[2])
                self.Graph[int(line_list[1])][int(line_list[0])] = int(line_list[2])
                # Initialise part 3 graph
                n = len(self.Graph)
                self.iceGraph[int(line_list[0])][int(line_list[1])] = int(line_list[2])
                self.iceGraph[int(line_list[1])][int(line_list[0])] = int(line_list[2])
                self.iceGraph[n + int(line_list[0])][n + int(line_list[1])] = int(line_list[2])
                self.iceGraph[n + int(line_list[1])][n + int(line_list[0])] = int(line_list[2])
                self.iceGraph[2*n + int(line_list[0])][2*n + int(line_list[1])] = int(line_list[2])
                self.iceGraph[2*n + int(line_list[1])][2*n + int(line_list[0])] = int(line_list[2])

            # Ensure first line not visited again
            line_checker = 1

        file.close()                                # Close the file

    def shallowest_spanning_tree(self):
        """
        Finds the 'most convenient suburb', aka, the vertex the least maximumn distance from all places

        @param self         The graph instance we are referencing
        @return [tuple]     Contains the index of the vertex and its min depth as a tuple
        @complexity         Time complexity is O(V^3) where V is the number of vertices in the graph
                            (As O(V^2) and 0(V) are both bounded above by 0(V^3) as V -> Infinity)
        """
        # Make an array that has only edge as 1s and others as infs - O(V^2)
        n = len(self.Graph)         # Get number of vertices
        swFW = [[n for _ in range(n)] for _ in range(n)]         # Create array; Infinity is n here as that's the
                                                                 # futhest any two vertices can be from each other
        for i in range(n):          # Loop over all of the graph array
            for j in range(n):
                if self.Graph[i][j] != None:
                    swFW[i][j] = 1
                if i == j:
                    swFW[i][j] = 0

        # Do the FW algorithm main loop - O(V^3)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if swFW[i][j] > swFW[i][k] + swFW[k][j]:
                        swFW[i][j] = swFW[i][k] + swFW[k][j]

        # Go through and find the minimum distance for each vertex - O(V^2)
        tot_spans = [0 for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if swFW[i][j] > tot_spans[i]:
                    tot_spans[i] = swFW[i][j]

        # Go through and find the min dist vertex: - O(V)
        mindex = 0
        mdepth = tot_spans[0]
        for i in range(n):
            if tot_spans[i] < mdepth:
                mindex = i
                mdepth = tot_spans[i]

        # Return required values
        return (mindex, mdepth)

    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        """
        Finds the shortest path including two detours - to get ice and icecream

        @param self             The instance of the class
        @param home             The starting vertex
        @param destination      The end vertex of the path
        @param ice_locs         The locations of the ice shop vertices
        @param ice_cream_locs   The ice cream shop vertices
        @return [tuple]         The distance and the path as required by the question
        @complexity             Time Complexity: O(E * log(V)) where V is the number of vertices and E is the number of
                                edges. As O(E) is bound above by O(E * log(V)) this is the value we are concerned with.
        """
        # Set the destination - note this is raw destination plus 2 n
        true_destination = destination + 2*len(self.Graph)

        # Insert ice locations into ice graph - O(V) < O(E)
        n = len(self.Graph)
        for i in range(len(ice_locs)):
            self.iceGraph[ice_locs[i]][ice_locs[i] + n] = 0

        # Insert icr cream locations into ice graph - O(V) < O(E)
        for i in range(len(ice_cream_locs)):
            self.iceGraph[ice_cream_locs[i] + n][ice_cream_locs[i] + 2*n] = 0

        # Call ice_dijkstra's on the ice graph - O(E * log(V))
        distance, path = self.ice_dijkstra(home, true_destination)

        # Set ice locations to None in ice graph - O(V) < O(E)
        for i in range(len(ice_locs)):
            self.iceGraph[ice_locs[i]][ice_locs[i] + n] = None

        # Set ice cream locations to None in ice graph - O(V) < O(E)
        for i in range(len(ice_cream_locs)):
            self.iceGraph[ice_cream_locs[i] + n][ice_cream_locs[i] + 2*n] = None

        # Augment Path to work correctly
        true_path = [path[0]]
        for i in range(1, len(path)):
            curloc = path[i]
            while curloc >= n:
                curloc = curloc - (n)
            if true_path[-1] != curloc:
                true_path.append(curloc)

        # return our required values
        return distance, true_path


    def ice_dijkstra(self, home, destination):
        """
        Implementation of dijkstra's using heap from heapq on our icegraph

        @param self             The instance of the class
        @param home             The starting vertex
        @param destination      The destination vertex
        @return [tuple]         The distance and the path
        @complexity             Time Complexity: O(E * log(V)) with min heap, as is stated in the lecture notes
        """
        # n is 3V
        n = len(self.iceGraph)

        # Priority is simplest format
        Q = [(0, home)]

        # Initialising the distance and path vertices
        p = [None] * n
        d = [float('inf')] * n
        d[home] = 0

        # Main loop, for while there are things in the queue
        while len(Q) != 0:
            (cost, u) = heapq.heappop(Q)

            # Checking the edge weights to see if we need to update
            for v in range(n):
                if self.iceGraph[u][v] is not None:
                    if d[v] > d[u] + self.iceGraph[u][v]:
                        d[v] = d[u] + self.iceGraph[u][v]       # Update distance
                        p[v] = u                                # Update path
                        heapq.heappush(Q, (d[v], v))            # Push from heap

        # Iterate over our path list to get the exact path taken
        i = p[destination]
        path = [destination]
        while i is not None:
            path = [i] + path
            i = p[i]

        # Return required values
        return d[destination], path


# Basic testing - proper testing done externally

gfile = "test3.txt"
test_graph = Graph(gfile)
dist = test_graph.shortest_errand(0, 8, [1,5,8], [4,6])
print(dist)
dist1 = test_graph.shortest_errand(0, 7, [1,5,8], [4,6])
print(dist1)
dist15 = test_graph.shortest_errand(0, 2, [1,5,8], [4,6])
print(dist15)
dist2 = test_graph.shortest_errand(0, 8, [1,5,8], [4,6])
print(dist2)






