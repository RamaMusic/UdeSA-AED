from graph import Graph
import time as casio


page_graph = Graph()

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
        
# Punto 1
# Start measuring time
start = casio.time()

number_of_wcc = page_graph.getNumberOfWCC()
biggest_wcc_size = page_graph.getBiggestWCC()

# Stop measuring time
end = casio.time()

print(f"Time elapsed: {end - start}s")

print(f"Number of weakly connected components: {number_of_wcc}")
print(f"Size of the biggest weakly connected component: {biggest_wcc_size}")

# Punto 2
# Como mi grafo tiene 875713 vertices, no puedo calcular el tiempo que me llevaría recorrer todos los caminos mínimos; pero puedo tomar una muestra de tamaño N y calcular el promedio de los caminos mínimos de esa muestra, después multiplicar ese promedio por el total de caminos mínimos posibles para obtener una estimación del tiempo que me llevaría recorrer todos los caminos.
n_samples = 1000
samples_seed = 42
_, mean, total = page_graph.getShortestPathSamples(n_samples, samples_seed)
print(f"Mean of the shortest path between {n_samples} samples: {mean}")