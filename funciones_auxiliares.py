#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
from ciudad import *
#Modulos de Python
import sys
import random
import math

def filtrar_infinitos(distancia):
    for v in distancia:
        if distancia[v] == math.inf: distancia.pop(v)

def ordenar_vertices(distancia):
    """Los vertices se ordenan 'solos' al pasarlos a una lista"""
    lista = []
    for v in distancia:
        lista.insert(0, v)
    print(lista)
    return lista

def centralidad_(grafo):
    cent = {}
    for v in grafo: cent[v] = 0
    for v in grafo:
        # hacia todos los demas vertices
        distancia, padre = dijkstra(grafo, v)
        cent_aux = {}
        for w in grafo: cent_aux[w] = 0

        filtrar_infinitos(distancia)
        vertices_ordenados = ordenar_vertices(distancia)
        for w in vertices_ordenados:
            if w == v: continue
            cent_aux[padre[w]] += 1 + cent_aux[w]
        # le sumamos 1 a la centralidad de todos los vertices que se encuentren en
        # el medio del camino
        for w in grafo:
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def imprimir_resultado(camino):
    for elem in range(len(camino)-1):
        print(camino[elem], end=" -> ")
    print(camino[len(camino)-1])

def cargar_ciudades_y_aeropuertos(archivo):
    ciudades = {}
    aeropuertos = {}
    with open(archivo) as aeros_csv:
        for linea in aeros_csv:
            linea = linea.replace('\n', '')
            separado = linea.split(",")
            if not separado[0] in ciudades:
                ciudades[separado[0]] = Ciudad()
            ciudades[separado[0]].agregar_aeropuerto(separado[1], separado[2], separado[3])
            aeropuertos[separado[1]] = [separado[2], separado[3]]
    return ciudades, aeropuertos

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
    indice = -1
    if modo == "rapido": indice = 0
    elif modo == "barato": indice = 1
    
    if modo == -1: raise Exception("Error en el modo")

    for c in ciudades:
        for aeropuerto in ciudades[c]: grafo.agregar_vertice(aeropuerto)
            
    for v in vuelos:
        separado = v.split("|")
        grafo.agregar_arista(separado[0], separado[1], int(vuelos[v][indice]))
        grafo.agregar_arista(separado[1], separado[0], int(vuelos[v][indice]))
    return grafo

def vacaciones_aux(origen, vertice, grafo, recorrido, cantidad):
    """
    Auxiliar de vacaciones.
    Recibe un vertice de origen, un vertice, un grafo, la lista del 
    recorrido y la cantidad de lugares a visitar.
    Devuelve True en caso de exito con la lista modificada.
    Devuelve False en caso de no encontrar ruta.
    """
    if len(recorrido) == cantidad:
        return True

    for ady in grafo.adyacentes(vertice):
        if ady not in recorrido:
            if len(recorrido) == cantidad-1:
                if not origen in grafo.adyacentes(ady):
                    continue
            recorrido.append(ady)
            if vacaciones_aux(origen, ady, grafo, recorrido, cantidad):
                return True
    
    recorrido.pop()
    return False

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
