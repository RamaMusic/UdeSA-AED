from graph import Graph
import time as casio

def readGraph() -> Graph:
    """
    Reads the web-Google.txt file and returns a Graph object
    """
    page_graph = Graph()
    print("Reading web-Google.txt...")
    with open('web-Google.txt', 'r') as file:
        for l in file:
            if "# FromNodeId	ToNodeId" in l:
                break
        for l in file:
            if not l:
                break
            edge = tuple(int(v.replace("\n", "").replace("\t", "")) for v in l.split("\t"))
            for v in edge:
                if not page_graph.vertex_exists(v):
                    page_graph.add_vertex(str(v))
            page_graph.add_edge(str(edge[0]), str(edge[1]))
    print("Finished reading web-Google.txt")
    return page_graph

def processTime(start, end):
    # Create a function that prints the hours or minutes only if they are greater than 0, and the seconds always with 2 decimal places
    hours, remainder = divmod(end - start, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = round(seconds, 2)
    if hours > 0: # Espero que esto nunca se cumpla
        print(f"Time elapsed: {hours:.0f}h {minutes:.0f}m {seconds}s")
    elif minutes > 0:
        print(f"Time elapsed: {minutes:.0f}m {seconds}s")
    else:
        print(f"Time elapsed: {seconds}s")


def act1(page_graph):
    print("--------------------")
    print("         P1         ")
    print("--------------------")
    start = casio.time()
    
    print("Calculating number of weakly connected components and size of the biggest weakly connected component...")
    number_of_wcc = page_graph.getNumberOfWCC()
    biggest_wcc_size = page_graph.getBiggestWCC()

    print(f"Number of weakly connected components: {number_of_wcc}")
    print(f"Size of the biggest weakly connected component: {biggest_wcc_size}")
    
    end = casio.time()
    
    processTime(start, end)
    
    # Los resultados son: 
    # Number of weakly connected components: 2746 
    # Size of the biggest weakly connected component: 855802

def act2(page_graph):
    # Como mi grafo tiene 875713 vertices, no puedo calcular el tiempo que me llevaría recorrer todos los caminos mínimos; pero puedo tomar una muestra de tamaño N y calcular el promedio de los caminos mínimos de esa muestra, después multiplicar ese promedio por el total de caminos mínimos posibles para obtener una estimación del tiempo que me llevaría recorrer todos los caminos.
    
    print("--------------------")
    print("         P2         ")
    print("--------------------")
    
    start = casio.time()
    
    n_samples = 100
    samples_seed = 42
    print(f"Estimating time for all shortest paths with {n_samples} samples and seed {samples_seed}...")
    time = page_graph.estimateTimeForShortestPaths(n_samples, samples_seed)
    hours, remainder = divmod(time, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = round(seconds, 2)
    print(f"Estimated time: {hours}h {minutes}m {seconds}s")
    
    end = casio.time()
    
    processTime(start, end)
    
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
    
    # Results:
    # Number of triangles using a Directed Graph: 3,889,771
    # Number of triangles using an Undirected Graph: 13,391,903
if __name__ == "__main__":
    page_graph = readGraph()
    # act1(page_graph)
    # act2(page_graph)
    # act3(page_graph, undirected=False)