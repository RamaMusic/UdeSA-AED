from graph import Graph
import time as casio

from tqdm import tqdm

def readGraph() -> Graph:
    """
    Reads the web-Google.txt file and returns a Graph object
    """
    page_graph = Graph()
    print("Reading web-Google.txt...")
    total_lines = 5105044  # Accurate total number of lines in the file
    with open('tp4/web-Google.txt', 'r') as file:
        # Skip initial comment lines
        for l in file:
            if l.startswith("#"):
                total_lines -= 1  # Adjust total_lines for each comment line skipped
            else:
                break

        for l in tqdm(file, initial=1, total=total_lines):
            if l.startswith("#"):
                continue  # Skip any additional comment lines
            parts = l.strip().split("\t")
            if len(parts) == 2:
                source, target = parts
                if not page_graph.vertex_exists(source):
                    page_graph.add_vertex(source)
                if not page_graph.vertex_exists(target):
                    page_graph.add_vertex(target)
                page_graph.add_edge(source, target)
    print("Finished reading web-Google.txt")
    return page_graph

def processTime(start, end, message="Time elapsed: "):
    # Create a function that prints the hours or minutes only if they are greater than 0, and the seconds always with 2 decimal places
    hours, remainder = divmod(end - start, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = round(seconds, 2)
    if hours > 0: # Espero que esto nunca se cumpla
        print(message + f"{hours:.0f}h {minutes:.0f}m {seconds}s")
    elif minutes > 0:
        print(message + f"{minutes:.0f}m {seconds}s")
    else:
        print(message + f"{seconds}s")

def act1(page_graph: Graph):
    print("--------------------")
    print("         P1         ")
    print("--------------------")
    start = casio.time()
    
    print("Calculating number of weakly connected components and size of the biggest weakly connected component...")
    number_of_wcc, wcc_dict = page_graph.getNumberOfWCC()
    biggest_wcc_size = page_graph.getBiggestWCC(wcc=wcc_dict)

    print(f"Number of weakly connected components: {number_of_wcc}")
    print(f"Size of the biggest weakly connected component: {biggest_wcc_size}")
    
    end = casio.time()
    
    processTime(start, end)
    print()
    # Los resultados son: 
    # Number of weakly connected components: 2746 
    # Size of the biggest weakly connected component: 855802

def act2(page_graph: Graph):
    # Como mi grafo tiene 875713 vertices, no puedo calcular el tiempo que me llevaría recorrer todos los caminos mínimos; pero puedo tomar una muestra de tamaño N y calcular el promedio de los caminos mínimos de esa muestra, después multiplicar ese promedio por el total de caminos mínimos posibles para obtener una estimación del tiempo que me llevaría recorrer todos los caminos.
    
    print("--------------------")
    print("         P2         ")
    print("--------------------")
    
    start = casio.time()
    
    n = 100
    
    print(f"Estimating time for all shortest paths with {n} samples...")
    time = page_graph.estimateTimeForShortestPaths(n, seed=None)
    processTime(0, time, "Estimated time: ")
    
    end = casio.time()
    
    processTime(start, end)
    print()    
    # El resultado es: 
    # Estimated time: 328.0h 43.0m 20.89s
    
def act3(page_graph: Graph, undirected = False):
    print("--------------------")
    print("         P3         ")
    print("--------------------")
    
    start = casio.time()
    
    print("Calculating the number of triangles using a directed Graph...")
    n_triangles_directed = page_graph.getNumberOfTrianglesDirected()
    print(f"Number of triangles using a Directed Graph: {n_triangles_directed:,}")
    
    if undirected:
        print("Calculating the number of triangles using an undirected Graph...")
        n_trinagles_undirected = page_graph.getNumberOfTrianglesUndirected()
        print(f"Number of triangles using an Undirected Graph: {n_trinagles_undirected:,}")
        
    end = casio.time()
    
    processTime(start, end)
    print()    
    # Results:
    # Number of triangles using a Directed Graph: 3,889,771
    # Number of triangles using an Undirected Graph: 13,391,903
    
def act4(page_graph: Graph):
    print("--------------------")
    print("         P4         ")
    print("--------------------")
    
    # Acá nuevamente no puedo calcular el diámetro del grafo, pero puedo tomar N puntos de inicio e iterar buscando los caminos más largos comparándolos entre sí.
    
    start = casio.time()
    
    n = 10
    print(f"Estimating the diameter of the graph with {n} starting vertices...")
    diameter = page_graph.estimateGraphDiameter(n, seed=None, directed=False)
    print(f"Estimated diameter of the graph: {diameter}")
    
    end = casio.time()
    
    processTime(start, end)
    print()    
    # Estimated diameter of the graph: 24
    # Time elapsed: 6m 0.09s
    
def act5(page_graph: Graph):
    print("--------------------")
    print("         P5         ")
    print("--------------------")
    
    # Calculo el pageRank de los 10 primeros vértices
    start = casio.time()
    
    n = 10
    
    print(f"Finding the top {n} vertices with the highest PageRank...")
    
    print(page_graph.getTopPageRankVertices(n))
    end = casio.time()
    
    processTime(start, end)
    print() 
    
    # Results
    # Converged after 61 iterations, aborting...
    # Top vertices with the highest PageRank:
    # Vertex: 597621, PageRank: 0.000644356692909492
    # Vertex: 41909, PageRank: 0.0006425477256693725
    # Vertex: 163075, PageRank: 0.0006305999262383353
    # Vertex: 537039, PageRank: 0.0006269920571772538
    # Vertex: 384666, PageRank: 0.0005489073817720516
    # Vertex: 504140, PageRank: 0.0005337169626427533
    # Vertex: 486980, PageRank: 0.000505691228595806
    # Vertex: 605856, PageRank: 0.0005008187129537594
    # Vertex: 32163, PageRank: 0.0004970646588593843
    # Vertex: 558791, PageRank: 0.0004947016865199656

    # Time elapsed: 2m 8.08s
    
def act6(page_graph: Graph):
    print("--------------------")
    print("         P6         ")
    print("--------------------")
    
    start = casio.time()
    n = 2
    
    print(f"Estimating the graph's circunference with {n} samples...")
    circunference = page_graph.estimateGraphCircumference(n, seed=None)
    print(f"Estimated circunference of the graph: {circunference}")
    end = casio.time()
    
    processTime(start, end)
    print()
    
    
# Puntos extra

# def extra1(page_graph: Graph):
#     print("--------------------")
#     print("        Extra1      ")
#     print("--------------------")
    
#     # Programe una función genérica que extendiendo la definición del triángulo calcule la
#     # cantidad de polígonos de K lados. Haga un gráfico para mostrar la cantidad de
#     # polígonos por cantidad de lados, estimando aquellos que no pueda calcular. (+2
#     # puntos)
    
#     start = casio.time()
    
    
    
#     end = casio.time()
    
#     processTime(start, end)
#     print()
    
#     # Results
#     # Graph density: 1.0e-05
#     # Time elapsed: 0.0s

def extra2(page_graph: Graph, directed = False):
    print("--------------------")
    print("        Extra2      ")
    print("--------------------")
    
    start = casio.time()
    print("Calculating the graph's average clustering coefficient for an undirected graph...")
    clustering_coefficient = page_graph.average_clustering_coefficient_undirected()
    print(f"Average clustering coefficient for an undirected graph: {clustering_coefficient}")
    
    if directed:
        print("Calculating the graph's average clustering coefficient for a directed graph...")
        clustering_coefficient_directed = page_graph.average_clustering_coefficient_directed()
        print(f"Average clustering coefficient for a directed graph: {clustering_coefficient_directed}")
    
    end = casio.time()
    
    processTime(start, end)
    print()
    
    # Results
    # Average clustering coefficient for an undirected graph: 0.5142961475354295
    # Average clustering coefficient for a directed graph: 0.3651263215748557
    # Time elapsed: 16.24s
    
def extra3(page_graph: Graph):
    print("--------------------")
    print("        Extra3      ")
    print("--------------------")
    
    start = casio.time()
    n = 100
    print(f"Estimating the graph's betweenness centrality with {n} samples...")
    node, value = page_graph.betweenness_centrality(n, seed=None)
    print(f"Node with the highest betweenness centrality: {node}, Value: {value}")
    end = casio.time()
    
    processTime(start, end)
    print()
    
    # Results
    # Node with the highest betweenness centrality: 560622, Value: 48932.75
    # Time elapsed: 3m 42.17s
    
if __name__ == "__main__":
    page_graph = readGraph()
    
    # Actividades
    # act1(page_graph)
    # act2(page_graph)
    # act3(page_graph, undirected=False)
    # act4(page_graph)
    # act5(page_graph)
    # act6(page_graph)
    
    # Extras
    # extra1(page_graph)
    extra2(page_graph, directed=True)
    # extra3(page_graph)