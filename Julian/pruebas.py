from grafo import *
from cola import *
from pila import *
from heap import *
import math

def comparacion(x, y):
    if x > y: return 1
    if x < y: return -1
    return 0

def comparacion_arboles(x, y):
    if x[1] < y[1]: return 1
    if x[1] > y[1]: return -1
    return 0

def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    q = Cola()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    q.encolar(origen)
    while not q.esta_vacia():
        v = q.desencolar()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                q.encolar(w)
    return padres, orden

def armar_grafo1():

    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_vertice("G")
    grafo.agregar_vertice("H")
    grafo.agregar_arista("A","B", 1)
    grafo.agregar_arista("A","C", 1)
    grafo.agregar_arista("B","A", 1)
    grafo.agregar_arista("B","D", 1)
    grafo.agregar_arista("B","E", 1)
    grafo.agregar_arista("B","F", 1)
    grafo.agregar_arista("C","A", 1)
    grafo.agregar_arista("C","D", 1)
    grafo.agregar_arista("D","B", 1)
    grafo.agregar_arista("D","E", 1)
    grafo.agregar_arista("E","B", 1)
    grafo.agregar_arista("E","D", 1)
    grafo.agregar_arista("E","H", 1)
    grafo.agregar_arista("E","G", 1)
    grafo.agregar_arista("F","B", 1)
    grafo.agregar_arista("G","E", 1)
    grafo.agregar_arista("G","H", 1)
    grafo.agregar_arista("H","E", 1)
    grafo.agregar_arista("H","G", 1)
    return grafo

def armar_grafo2():

    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_vertice("G")
    grafo.agregar_arista("A","B", 1)
    grafo.agregar_arista("B","C", 1)
    grafo.agregar_arista("B","F", 1)
    grafo.agregar_arista("D","B", 1)
    grafo.agregar_arista("D","F", 1)
    grafo.agregar_arista("F","C", 1)
    grafo.agregar_arista("F","G", 1)
    return grafo

def armar_grafo3():
    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_arista("A","B", 2)
    grafo.agregar_arista("A","E", 1)
    grafo.agregar_arista("A","D", 6)
    grafo.agregar_arista("B","A", 2)
    grafo.agregar_arista("B","F", 8)
    grafo.agregar_arista("C","F", 1)
    grafo.agregar_arista("C","D", 2)
    grafo.agregar_arista("D","A", 6)
    grafo.agregar_arista("D","E", 3)
    grafo.agregar_arista("D","C", 2)
    grafo.agregar_arista("E","D", 3)
    grafo.agregar_arista("E","A", 1)
    grafo.agregar_arista("F","B", 8)
    grafo.agregar_arista("F","C", 1)

    return grafo

def armar_grafo4():
    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_arista("A","B", 1)
    grafo.agregar_arista("A","C", 7)
    grafo.agregar_arista("A","E", 2)
    grafo.agregar_arista("A","D", 5)
    grafo.agregar_arista("B","A", 1)
    grafo.agregar_arista("B","C", 5)
    grafo.agregar_arista("B","D", 6)
    grafo.agregar_arista("C","A", 7)
    grafo.agregar_arista("C","D", 4)
    grafo.agregar_arista("C","B", 5)
    grafo.agregar_arista("D","B", 6)
    grafo.agregar_arista("D","C", 4)
    grafo.agregar_arista("D","A", 5)
    grafo.agregar_arista("D","F", 8)
    grafo.agregar_arista("E","A", 2)
    grafo.agregar_arista("E","F", 7)
    grafo.agregar_arista("F","E", 7)
    grafo.agregar_arista("F","D", 8)

    return grafo

def orden_topologico(grafo, vertice):
    grados = {}
    for v in grafo: grados[v] = 0
    for v in grafo:
        for w in grafo.adyacentes(v):
            grados[w] += 1
    q = Cola()
    for v in grafo:
        if grados[v] == 0: q.encolar(v)
    resul = []
    while not q.esta_vacia():
        v = q.desencolar()
        resul.append(v)
        for w in grafo.adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0: q.encolar(w)
    return resul

def reconstruir_camino(origen, destino, padre):
    resultado = []
    while destino != origen:
        resultado.insert(0, destino)
        destino = padre[destino]
    resultado.insert(0, origen)
    return resultado

def dijkstra(grafo, origen, destino):

    dist = {}
    padre = {}

    for v in grafo: dist[v] = math.inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap(comparacion)
    q.encolar([origen, dist[origen]])
    while not q.esta_vacia():
        v = q.desencolar()[0]
        if v == destino: return reconstruir_camino(origen, destino, padre)
        for w in grafo.adyacentes(v):
            if dist[v] + grafo.peso_union(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_union(v, w)
                padre[w] = v
                q.encolar([w, dist[w]])
    return padre, dist

def prim(grafo, vertice):

    visitados = set()
    visitados.add(vertice)
    q = Heap(comparacion_arboles)

    for w in grafo.adyacentes(vertice):
        q.encolar([(vertice, w), grafo.peso_union(vertice, w)])
    arbol = grafo_crear(grafo.obtener_vertices())

    while not q.esta_vacia():
        (v,w) = q.desencolar()[0]
        if w in visitados: continue
        arbol.agregar_arista(v, w, grafo.peso_union(v, w))
        visitados.add(w)
        for x in grafo.adyacentes(w):
            if x not in visitados: q.encolar([(w, x), grafo.peso_union(w, x)])
    return arbol


def grafo_crear(vertices):
    grafo = Grafo()
    for v in vertices:
        grafo.agregar_vertice(v)
    return grafo


def main():

    grafo = armar_grafo4()

    for v in grafo:
        print(v)
    #arbol = prim(grafo, "A")
    """
    for v in arbol.vertices:
        print(v + ":" + str(arbol.vertices[v]))
    """
    """
    for v in padres:
        print(v + ":" + str(padres[v]) + ":" + str(orden[v]))

    """
    """
    #print(grafo)
    for v in grafo.vecinos:
        print(v + ":" + str(grafo.vecinos[v]))

    print("/" * 50)
    """
main()
