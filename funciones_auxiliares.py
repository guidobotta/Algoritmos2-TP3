#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
from ciudad import *
#Modulos de Python
import sys
import math

def imprimir_resultado(camino):
    for a in range(len(camino)-1):
        print(camino[a], end=" -> ")
    print(camino[len(camino)-1])

def cargar_ciudades(archivo):
    ciudades = {}
    with open(archivo) as aeros_csv:
        for linea in aeros_csv:
            linea = linea.replace('\n', '')
            separado = linea.split(",")
            if not separado[0] in ciudades:
                ciudades[separado[0]] = Ciudad()
            ciudades[separado[0]].agregar_aeropuerto(separado[1], separado[2], separado[3])
    return ciudades

def clave_vuelo(aeropuerto1, aeropuerto2):
    return aeropuerto1 + "|" + aeropuerto2

def cargar_vuelos(archivo):
    vuelos = {}
    with open(archivo) as vuelos_csv:
        for linea in vuelos_csv:
            linea = linea.replace('\n', '')
            separado = linea.split(",")
            clave = clave_vuelo(separado[0], separado[1])
            vuelos[clave] = (separado[2], separado[3], separado[4])
    return vuelos

def armar_grafo(ciudades, vuelos, modo):
    grafo = Grafo()
    indice = 0
    if modo == "barato": indice = 1

    for c in ciudades:
        for aeropuerto in ciudades[c]: grafo.agregar_vertice(aeropuerto)
    for v in vuelos:
        separado = v.split("|")
        grafo.agregar_arista(separado[0], separado[1], int(vuelos[v][indice]))
        grafo.agregar_arista(separado[1], separado[0], int(vuelos[v][indice]))
    return grafo

def comparacion(x, y):
    if x[1] < y[1]: return 1
    if x[1] > y[1]: return -1
    return 0

def reconstruir_camino(origen, destino, padre, distancia):
    resultado = []
    distancia_total = distancia[destino]
    while destino != origen:
        resultado.insert(0, destino)
        destino = padre[destino]
    resultado.insert(0, origen)
    return resultado, distancia_total

def dijkstra(grafo, origen, ciudad_destino):

    dist = {}
    padre = {}

    for v in grafo: dist[v] = math.inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap(comparacion)
    q.encolar([origen, dist[origen]])
    while not q.esta_vacia():
        v = q.desencolar()[0]
        if v in ciudad_destino: return reconstruir_camino(origen, v, padre, dist)
        for w in grafo.adyacentes(v):
            if dist[v] + grafo.peso_union(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_union(v, w)
                padre[w] = v
                q.encolar([w, dist[w]])
    #Devolvemos algo acá?

def bfs(grafo, origen, destino):
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
                if w in destino: return reconstruir_camino(origen, w, padres, orden)
                q.encolar(w)
    #Devolvemos algo acá?
