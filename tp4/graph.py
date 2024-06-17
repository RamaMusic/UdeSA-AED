from typing import Optional, Any, List

from collections import deque
import numpy as np
import time
from tqdm import tqdm

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
        for vertex in tqdm(undirected_graph._graph):  # Step 2: Wrap with tqdm
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
    
    def estimateTimeForShortestPaths(self, n_samples, seed) -> float:
        """
        Estimate the time for all shortest paths
        
        Args:
            n_samples: the number of samples
            seed: the seed for the random generator
            
        Returns:
            the estimated time
        """
        
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
    

    def estimateGraphDiameter(self, n_samples, seed) -> int:
        """
        Estimate the diameter of the graph
        
        Args:
            n_samples: the number of samples
            seed: the seed for the random generator
            
        Returns:
            the estimated diameter of the graph
        """
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
            