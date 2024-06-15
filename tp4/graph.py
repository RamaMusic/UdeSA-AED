from typing import Optional, Any, List
import numpy as np

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
        for vertex in undirected_graph._graph:
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
    
    def getBiggestWCC(self, onlyLenght = True) -> int:
        """
        Get the biggest weakly connected component.
        If onlyLenght is True, return the length of the biggest WCC
        """
        wcc = self.getWCC()
        return max(wcc, key=len) if not onlyLenght else len(max(wcc, key=len))
    
    def getNumberOfWCC(self) -> int:
        """
        Get the number of weakly connected components
        """
        wcc = self.getWCC()
        return len(wcc)
    
    # def bfs