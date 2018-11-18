from grafo import *
from cola import *
from pila import *
from heap import *

def comparacion(x, y):
    if x > y: return 1
    if x < y: return -1
    return 0

def main():

    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_arista("A","B", 1)
    grafo.agregar_arista("B","A", 2)
    grafo.agregar_arista("A","C", 3)
    grafo.agregar_arista("C","E", 1)
    grafo.agregar_arista("B","F", 2)
    grafo.agregar_arista("F","D", 3)
    grafo.agregar_arista("D","B", 1)
    grafo.agregar_arista("D","A", 2)
    grafo.agregar_arista("F","B", 3)
    grafo.agregar_arista("E","A", 2)
    grafo.agregar_arista("E","B", 3)

    #print(grafo)
    for v in grafo.adyacentes:
        print(v + ":" + str(grafo.adyacentes[v]))

    print("/" * 50)
    #grafo.eliminar_vertice("B")
    grafo.eliminar_arista("A", "B")

    for v in grafo.adyacentes:
        print(v + ":" + str(grafo.adyacentes[v]))
    #print(grafo.adyacentes["A"])

main()
