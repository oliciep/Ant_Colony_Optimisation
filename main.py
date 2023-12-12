# Importing relevant libraries
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from read_dat import read_distance_matrix, read_flow_matrix

# read the distance and flow matrices from the input file
contents = open("Uni50a.dat").read()
n = contents.split()[0]
D = read_distance_matrix('Uni50a.dat')
F = read_flow_matrix('Uni50a.dat')

# Main vertex class
class Vertex:
    # Initialises vertex attributes
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    # Allows for vertex to be returned in string form
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    # Adds connected nodes to a list
    def add_neighbor(self, neighbor, distance=0, flow=0, pheromone=0):
        self.adjacent[neighbor] = distance, flow, pheromone

    # Gets all the connected nodes that current node is connected to.
    def get_connections(self):
        return self.adjacent.keys()

    # Gets id of current node.
    def get_id(self):
        return self.id

    #Gets attributes of adjacent neighbour
    def get_attributes(self, neighbor):
        return self.adjacent[neighbor]

# Main class for the construction graph, allows for graph to be created
class Graph:
    # Initialises the construction graph
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    # Allows for iteration over the graph
    def __iter__(self):
        return iter(self.vert_dict.values())

    #Creates nodes where ants will path to
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    # Retrieves dictionary of vertices
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None


    # Initialises all the edges to be pathed upon
    def add_edge(self, frm, to, distance, flow, pheromone):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], distance, flow, pheromone)

    # Gets all the vertices
    def get_vertices(self):
        return self.vert_dict.keys()

# Main ant class, where ants are created and then sent on their paths
class Ant:
    def __init__(self):
        self.id = id
        self.nodes_visited = []
        self.current_node = con_graph.get_vertex(20)
        self.fitness = 0

    # This function handles the main movement of the ants, and where they path
    def move_ant(self, current_node):
        while len(self.nodes_visited) != 50:
            possible_paths = []
            paths = []
            self.nodes_visited.append(int(current_node.get_id()))
            for i in range(0, 50):
                if i in self.nodes_visited:
                    pass
                else:
                    paths.append(i)
            for i in current_node.get_connections():
                if int(i.id) in self.nodes_visited:
                    pass
                else:
                    possible_paths.append(current_node.get_attributes(i)[2] * random.uniform(0, 1))
            if len(paths) != 0:
                chosen_path = random.choices(paths, possible_paths)
                path = int(''.join(str(i) for i in chosen_path))
                for i in current_node.get_connections():
                    if int(i.id) == path:
                        self.fitness += int(current_node.get_attributes(i)[0]) * (int(current_node.get_attributes(i)[1]))
                self.move_ant(con_graph.get_vertex(int(path)))
        return self.fitness

    # This function deposits pheromones onto edges once the path is completed
    def deposit_pheromone(self):
        for i in range(len(self.nodes_visited) - 1):
            node_index = int(self.nodes_visited[i])
            #print(node_index)
            node_1 = con_graph.get_vertex(node_index)
            #print(node_1)
            node_2_index = self.nodes_visited[i+1]
            node_2 = con_graph.get_vertex(node_2_index)
            for i in node_1.get_connections():
                if int(i.id) == node_2_index:
                    val1 = node_1.adjacent[i][0]
                    val2 = node_1.adjacent[i][1]
                    val3 = node_1.adjacent[i][2] + 1 /self.fitness
                    valtup = val1, val2, val3
                    node_2.adjacent[i] = valtup
            for j in node_2.get_connections():
                if int(j.id) == node_index:
                    val1 = node_2.adjacent[j][0]
                    val2 = node_2.adjacent[j][1]
                    val3 = node_2.adjacent[j][2] + 1 / self.fitness
                    valtup = val1, val2, val3
                    node_1.adjacent[i] = valtup
                    #print(node_1.get_attributes(i)[2], " this is that")
                    #print(node_2.get_attributes(i)[2], " this is that")
            #print(node_1.get_attributes(i)[2] , " this is that")
            #print(node_1.adjacent[i][2])

# This function allows for the evaporating of the pheromone on edges
def evaporate_links(e):
    for v in con_graph:
        for w in v.get_connections():
            #print("hi")
            val1 = v.adjacent[w][0]
            val2 = v.adjacent[w][1]
            val3 = v.adjacent[w][2] * e
            valtup = val1, val2, val3
            v.adjacent[w] = valtup
            #print(v.adjacent[w][2])

# Here is the main module of the code, which instantiates the ant colony optimisation problem
con_graph = Graph()
for i in range(0,50):
    con_graph.add_vertex(i)
    for j in range(0, 50):
        con_graph.add_edge(i, j, D[i][j], F[i][j], 1)

nodes_visited = []
ants = list()
best_fitness = 1000000000
xpoints = []
for k in range(500):
    for i in range(10):
        nodes_visited = []
        ants.append(Ant())
        ants[i].move_ant(con_graph.get_vertex(0))
        if ants[i].fitness < best_fitness:
            best_fitness = ants[i].fitness
    for i in range(10):
        ants[i].deposit_pheromone()
    evaporate_links(1)
    ants = list()
    print(best_fitness)
    xpoints.append(best_fitness)

ypoints = []
[ypoints.append(x) for x in range(len(xpoints))]
plt.plot(ypoints, xpoints)
plt.show()
