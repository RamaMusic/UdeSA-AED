from typing import Optional, Any, List

from collections import deque
import numpy as np
import time
from tqdm import tqdm

from collections import defaultdict


class Graph:
    """
    Graph class
    """
    def __init__(self):
        self._graph = {}

    def add_vertex(self, vertex: str, data: Optional[Any]=None) -> None:
        """
        Adds a vertex to the graph
        :param vertex: the vertex name
        :param data: data associated with the vertex
        """
        if vertex not in self._graph:
            self._graph[vertex] = {'data': data, 'neighbors': {}}

    def add_edge(self, vertex1: str, vertex2: str, data: Optional[Any]=None) -> None:
        """
        Adds an edge to the graph
        :param vertex1: vertex1 key
        :param vertex2: vertex2 key
        :param data: the data associated with the vertex
        """
        if not vertex1 in self._graph or not vertex2 in self._graph:
            raise ValueError("The vertexes do not exist")
        self._graph[vertex1]['neighbors'][vertex2] = data

    def get_neighbors(self, vertex) -> List[str]:
        """
        Get the list of vertex neighbors
        :param vertex: the vertex to query
        :return: the list of neighbor vertexes
        """
        if vertex in self._graph:
            return list(self._graph[vertex]['neighbors'].keys())
        else:
            return []

    def get_vertex_data(self, vertex: str) -> Optional[Any]:
        """
        Gets  vertex associated data
        :param vertex: the vertex name
        :return: the vertex data
        """
        if self.vertex_exists(vertex):
            return self._graph[vertex]['data']
        else:
            return None

    def get_edge_data(self, vertex1: str, vertex2: str) -> Optional[Any]:
        """
        Gets the vertexes edge data
        :param vertex1: the vertex1 name
        :param vertex2: the vertex2 name
        :return: vertexes edge data
        """
        if self.edge_exists(vertex1, vertex2):
            return self._graph[vertex1]['neighbors'][vertex2]
        raise ValueError("The edge does not exist")

    def print_graph(self) -> None:
        """
        Prints the graph
        """
        for vertex, data in self._graph.items():
            print("Vertex:", vertex)
            print("Data:", data['data'])
            print("Neighbors:", data['neighbors'])
            print("")

    def vertex_exists(self, vertex: str) -> bool:
        """
        If contains a vertex
        :param vertex: the vertex name
        :return: boolean
        """
        return vertex in self._graph

    def edge_exists(self, vertex1: str, vertex2: str) -> bool:
        """
        If contains an edge
        :param vertex1: the vertex1 name
        :param vertex2: the vertex2 name
        :return: boolean
        """
        return vertex1 in self._graph and vertex2 in self._graph[vertex1]['neighbors']

    def create_undirected_graph(self) -> 'Graph':
        """
        Creates an undirected graph
        """
        newGraph = Graph()
        for vertex, data in self._graph.items():
            newGraph.add_vertex(vertex, data['data'])
            for neighbor, edge_data in data['neighbors'].items():
                newGraph.add_vertex(neighbor, self._graph[neighbor]['data'])
                newGraph.add_edge(vertex, neighbor, edge_data)
                newGraph.add_edge(neighbor, vertex, edge_data)
                
        return newGraph
        
    def getWCC(self) -> List[List[str]]:
        """
        Get the weakly connected components
        """
        undirected_graph = self.create_undirected_graph()
        visited = {vertex: False for vertex in undirected_graph._graph}
        wcc = []
        for vertex in tqdm(undirected_graph._graph):
            if not visited[vertex]:
                wcc.append(self.isWCC(vertex, visited, undirected_graph))
        return wcc
    
    def isWCC(self, vertex, visited, undirected_graph) -> List[str]:
        """
        Check if the graph is weakly connected
        """
        wcc = []
        stack = [vertex]
        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                visited[vertex] = True
                wcc.append(vertex)
                stack.extend(undirected_graph.get_neighbors(vertex))
        return wcc
    
    def getBiggestWCC(self, onlyLenght = True, wcc: dict = None) -> int:
        """
        Get the biggest weakly connected component.
        If onlyLenght is True, return the length of the biggest WCC
        """
        if not wcc:
            wcc = self.getWCC()
        return max(wcc, key=len) if not onlyLenght else len(max(wcc, key=len))
    
    def getNumberOfWCC(self, returnDict: bool = False) -> int:
        """
        Get the number of weakly connected components
        """
        wcc = self.getWCC()
        return len(wcc) if not returnDict else len(wcc), wcc
    
    def bfs(self, start) -> dict:
        """
        Breadth First Search.
        
        Args:
            start: the starting vertex
        
        Returns:
            the distances from the starting vertex to all other vertices
        """

        distances = {v: float('inf') for v in self._graph}
        distances[start] = 0
        
        parents = {v: None for v in self._graph}
        
        q = deque([start])
        
        while q:
            vertex = q.popleft()
            for neighbor in self.get_neighbors(vertex):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[vertex] + 1
                    parents[neighbor] = vertex
                    q.append(neighbor)
                    
        return distances, parents
    
    def estimateTimeForShortestPaths(self, n_samples, seed = None) -> float:
        """
        Estimate the time for all shortest paths
        
        Args:
            n_samples: the number of samples
            seed: the seed for the random generator
            
        Returns:
            the estimated time
        """
        if seed:
            np.random.seed(seed)
        
        samples = np.random.choice(list(self._graph.keys()), n_samples)

        times = []
        for node in tqdm(samples):  # Step 2: Wrap with tqdm
            start = time.time()
            self.bfs(node)
            end = time.time()
            times.append(end - start)

        avg_time = np.mean(times)

        return avg_time * len(self._graph)
    
    def getNumberOfTrianglesUndirected(self) -> int:
        """
        Get the number of triangles in the undirected graph.
        
        Returns:
            The number of triangles in the undirected graph.
        """
        undirected_graph = self.create_undirected_graph()
        triangles = 0
        for vertex in tqdm(undirected_graph._graph):  # Step 2: Wrap with tqdm
            neighbors = sorted(list(undirected_graph.get_neighbors(vertex)))
            for i, neighbor in enumerate(neighbors):
                if neighbor > vertex:
                    mutual_neighbors = set(neighbors[i+1:])  # Only consider neighbors greater than the current neighbor
                    for mutual_neighbor in mutual_neighbors.intersection(undirected_graph.get_neighbors(neighbor)):
                        triangles += 1
        return triangles
    
    def getNumberOfTrianglesDirected(self) -> int:
        """
        Get the number of triangles in the directed graph considering only cycles like a->b->c->a.

        Returns: 
            The number of triangles in the graph.
        """
        triangles = 0
        for vertex in tqdm(self._graph): 
            neighbors = self.get_neighbors(vertex)
            for neighbor in neighbors:
                mutual_neighbors = self.get_neighbors(neighbor)
                for mutual_neighbor in mutual_neighbors:
                    if vertex in self.get_neighbors(mutual_neighbor):
                        triangles += 1
        return triangles // 3  # Cada triángulo se cuenta 3 veces, una por cada vértice
    
    def findLongestPathBetween(self, start, end) -> List[str]:
        """
        Find the longest path between two vertices
        
        Args:
            start: the starting vertex
            end: the ending vertex
            
        Returns:
            the longest path between the two vertices
        """
        distances, parents = self.bfs(start)
        if distances[end] == float('inf'):
            return []
        
        path = [end]
        while path[-1] != start:
            path.append(parents[path[-1]])
        return path[::-1]
    

    def estimateGraphDiameterBetweenTwoRandomNodes(self, n_samples, seed = None) -> int:
        """
        Estimate the diameter of the graph between two random nodes
        
        Args:
            n_samples: the number of samples
            seed: the seed for the random generator
            
        Returns:
            the estimated diameter of the graph
        """
        if seed:
            np.random.seed(seed)
        
        lengths = []
        
        with tqdm(total=n_samples) as pbar: 
            while len(lengths) < n_samples:
                samples = np.random.choice(list(self._graph.keys()), 2)
                path = self.findLongestPathBetween(samples[0], samples[1])
                if path:
                    lengths.append(len(path))
                    pbar.update(1)
        
        return max(lengths)
    
    
    def estimateGraphDiameter(self, n_samples, seed = None, directed = False) -> int:
        """
        Estimate the diameter of the graph starting from one random node and then iterating over the longest path, repeating this process n_samples times and then returning the maximum distance found between all the samples.
        
        Args:
            n_samples: the number of samples
            seed: the seed for the random generator
            
        Returns:
            the estimated diameter of the graph
        """
        if seed:
            np.random.seed(seed)
            
        if not directed:
            graph = self.create_undirected_graph()
            
        max_distance = 0    
        
        for _ in tqdm(range(n_samples)):
            
            sample = np.random.choice(list(graph._graph.keys()))
            
            for _ in range(n_samples):
                distances, _ = graph.bfs(sample) 
                distances = {k: v for k, v in distances.items() if v != float('inf')}
                
                max_distance = max(max_distance, max(distances.values()))
                
                max_vertex = max(distances, key=distances.get)
                sample = max_vertex
                
        return max_distance
            
    def transposeGraph(self) -> 'Graph':
        """
        Transpose the graph
        """
        transposed = Graph()
        for vertex in self._graph:
            transposed.add_vertex(vertex, self._graph[vertex]['data'])
        for vertex in self._graph:
            for neighbor in self._graph[vertex]['neighbors']:
                transposed.add_edge(neighbor, vertex, self._graph[vertex]['neighbors'][neighbor])
        return transposed
    
    def getTopPageRankVertices(self, top_n: int, iters = 100, tol = 1e-6, damping = 0.85) -> List[str]:
        """
        Shows the top N vertices with the highest PageRank
        
        Args:
            top_n: the number of vertices to show
            iters: the number of iterations
            tol: the tolerance
            damping: the damping factor
            
        Returns:
            the top N vertices with the highest PageRank
        """
        
        page_rank = self.pageRank(damping, tol, iters)
        
        shorted = sorted(page_rank, key=page_rank.get, reverse=True)[:top_n]
        
        string = ""
        
        string += "Top vertices with the highest PageRank:\n"
        for vertex in shorted:
            string += f"Vertex: {vertex}, PageRank: {page_rank[vertex]}\n"
        
        return string
    
    def pageRank(self, damping=0.85, tol=1e-6, iters=100) -> dict:
        """
        PageRank algorithm
        
        Args:
            damping: the damping factor
            tol: the tolerance
            iters: the number of iterations
            
        Returns:
            the PageRank of the vertices
        """
        transposed = self.transposeGraph()
        n = len(self._graph)
        
        page_rank = {vertex: 1/n for vertex in self._graph}
        
        n_neighbors = {vertex: len(self.get_neighbors(vertex)) for vertex in self._graph}
        pointingToMe = {vertex: transposed.get_neighbors(vertex) for vertex in self._graph}
        
        for iteration in tqdm(range(1, iters + 1)):
            new_page_rank = {}
            for vertex in self._graph:
                rank = 0
                for neighbor in pointingToMe[vertex]:
                    rank += page_rank[neighbor] / n_neighbors[neighbor]
                new_page_rank[vertex] = (1 - damping) / n + damping * rank
                
            # Check convergence
            diff = sum(abs(new_page_rank[vertex] - page_rank[vertex]) for vertex in self._graph)
            if diff < tol:
                break
            
            page_rank = new_page_rank
            
        print(f"Converged after {iteration} iterations, aborting...")
            
        return page_rank
    
    def dfs(self, start) -> dict:
        """
        Perform a Depth First Search (DFS) starting from a given vertex.

        Args:
            start: The starting vertex.

        Returns:
            A tuple containing two dictionaries:
            - The first dictionary maps each vertex to its distance from the start.
            - The second dictionary maps each vertex to its parent in the DFS tree.
        """

        distances = {v: float('inf') for v in self._graph}
        parents = {v: None for v in self._graph}

        distances[start] = 0
        
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            for neighbor in self.get_neighbors(vertex):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[vertex] + 1
                    parents[neighbor] = vertex
                    stack.append(neighbor)
                    
        return distances, parents
    
    def _find_cycle_with_length(self, start_node, visited, path_stack, cycle_length):
        stack = [(start_node, [start_node])]
        while stack:
            current_node, path = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                path_stack[current_node] = path
                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
                    elif neighbor in path_stack and neighbor in path:
                        cycle = path
                        if len(cycle) - cycle.index(neighbor) == cycle_length:
                            return cycle[cycle.index(neighbor):]
            elif current_node in path_stack and current_node in path:
                if len(path) - path.index(current_node) == cycle_length:
                    return path[path.index(current_node):]
                else:
                    return []
        return []

    def find_cycle_of_length(self, cycle_length=3, timeout=5):
        start_time = time.time()
        updates = timeout / 0.1  # Assuming an update every 0.1 seconds
        pbar = tqdm(total=updates, desc=f"Checking for cycles of length {cycle_length}", leave=False, unit="checks")
        cycle_found = False

        for node in self._graph:
            if time.time() - start_time > timeout:
                break
            visited = set()
            cycle = self._find_cycle_with_length(node, visited, {}, cycle_length)
            if cycle:
                cycle_found = True
                break
            # Update progress bar based on elapsed time
            elapsed = time.time() - start_time
            expected_updates = elapsed / 0.1
            while pbar.n < expected_updates:
                pbar.update(1)

        pbar.close()  # Close the progress bar regardless of the outcome

        # If a cycle is found, print a message instead of leaving the progress bar
        if cycle_found:
            print(f"\tCycle of length {cycle_length} found!")
            return cycle
        else:
            return[]

    def _cycle_length_worker(self, cycle_length, timeout):
        cycle = self.find_cycle_of_length(cycle_length, timeout)
        if cycle:
            return len(cycle)
        return 0

    def find_circumference(self, timeout=5):
        vertices = list(self._graph.keys())
        circumference = [0]

        def binary_search_cycle_length(low, high):
            if low > high:
                return
            mid = (low + high) // 2
            cycle_length = self._cycle_length_worker(mid, timeout)
            circumference[0] = max(circumference[0], cycle_length)
            if cycle_length == mid:
                binary_search_cycle_length(mid + 1, high)
            else:
                binary_search_cycle_length(low, mid - 1)

        binary_search_cycle_length(2, len(vertices))
        return circumference[0]
    
    # Puntos extra
    def average_clustering_coefficient_undirected(self) -> float:
        """
        Calculate the average clustering coefficient of the undirected graph.
        
        Returns:
            The average clustering coefficient of the undirected graph.
        """

        undirected_graph = self.create_undirected_graph()
        total_coefficient = 0
        precomputed_neighbors = {vertex: set(undirected_graph.get_neighbors(vertex)) for vertex in tqdm(undirected_graph._graph, desc="Precomputing Neighbors")}

        for _, neighbors in tqdm(precomputed_neighbors.items(), desc="Calculating coefficients"):
            n_neighbors = len(neighbors)
            if n_neighbors < 2:
                continue
            triangles = sum(len(precomputed_neighbors[neighbor].intersection(neighbors)) for neighbor in neighbors)
            total_coefficient += triangles / (n_neighbors * (n_neighbors - 1))

        return total_coefficient / len(undirected_graph._graph) if undirected_graph._graph else 0
    
    def average_clustering_coefficient_directed(self) -> float:
        """
        Calculate the average clustering coefficient of the directed graph.
        
        Returns:
            The average clustering coefficient of the directed graph.
        """
        total_coefficient = 0
        neighbors_cache = {vertex: set(self.get_neighbors(vertex)) for vertex in tqdm(self._graph, desc="Precomputing Neighbors")}
        
        for _, neighbors in tqdm(neighbors_cache.items(), desc="Calculating coefficients"):
            if len(neighbors) < 2:
                continue
            
            triangles = 0
            for neighbor in neighbors:
                mutual_neighbors = neighbors_cache[neighbor].intersection(neighbors)
                triangles += len(mutual_neighbors)
            
            triangles /= 2
            
            possible_triangles = len(neighbors) * (len(neighbors) - 1) / 2
            total_coefficient += triangles / possible_triangles if possible_triangles > 0 else 0

        return total_coefficient / len(self._graph) if self._graph else 0
    
    def betweenness_centrality(self, n_samples, seed=None) -> tuple:
        """
        Estimate the betweenness centrality of the graph with a given number of samples.
        
        Args:
            n_samples: The number of samples.
            seed: The seed for the random generator.
            
        Returns:
            The node with the highest betweenness centrality and its value.
        """
        if seed:
            np.random.seed(seed)
        
        betweenness = defaultdict(int)
        samples = np.random.choice(list(self._graph.keys()), n_samples)

        for node in tqdm(samples):
            _, parents = self.bfs(node)
            for vertex in parents:
                if parents[vertex] is not None:
                    current = vertex
                    while current is not None:
                        betweenness[current] += 1
                        current = parents[current]

        normalized_betweenness = {k: v / n_samples for k, v in betweenness.items()}

        max_node = max(normalized_betweenness, key=normalized_betweenness.get)
        max_value = normalized_betweenness[max_node]
         
        
        return max_node, max_value
    
    # a checkear
    def estimateKSidePolygons(self, k, seed=None) -> int:
        """
        Estimate the number of k-side polygons in the graph.
        
        Args:
            k: The number of sides of the polygon.
            seed: The seed for the random generator.
            
        Returns:
            The estimated number of k-side polygons in the graph.
        """
        if seed:
            np.random.seed(seed)
        
        polygons = 0
        for _ in tqdm(range(1000)):
            vertex = np.random.choice(list(self._graph.keys()))
            neighbors = self.get_neighbors(vertex)
            if len(neighbors) < k:
                continue
            for neighbor in neighbors:
                mutual_neighbors = self.get_neighbors(neighbor).intersection(neighbors)
                polygons += sum(1 for mutual_neighbor in mutual_neighbors if mutual_neighbor > vertex)
                
        return polygons // k
    
    # a checkear v2, código de ana
    def count_k_polygons(self, k: int, sample_nodes: List[str]) -> int:
            def dfs_find_polygons(start, current, length, visited):
                if length == k:
                    if current == start:
                        return 1
                    return 0
                
                if length > k:
                    return 0
                
                visited.add(current)
                polygons_count = 0

                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited or (neighbor == start and length + 1 == k):
                        polygons_count += dfs_find_polygons(start, neighbor, length + 1, visited)
                
                visited.remove(current)
                return polygons_count
            
            total_polygons = 0
            for node in sample_nodes:
                total_polygons += dfs_find_polygons(node, node, 0, set())

            # cada polígono se cuenta k veces, una por cada vértice, entonces divido por k
            return total_polygons // k
    
    # micol
    def checkIfPathExists(self, path: List[str]) -> bool:
        """
        Check if a path exists in the graph and forms a cycle.
        
        Args:
            path: The path to check.
            
        Returns:
            True if the path exists and forms a cycle, False otherwise.
        """
        path = path.copy()
        path.pop()
        for i in range(len(path) - 1):
            if not self.edge_exists(path[i], path[i+1]):
                return False
        # Check if there's an edge from the last node back to the first node to form a cycle
        return self.edge_exists(path[-1], path[0]) if path else False