#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
from ciudad import *
#Modulos de Python
import sys
import math


def filtrar_infinitos(distancia):
    for v in distancia:
        if distancia[v] == math.inf: distancia.pop(v)

def segundo_item(lista):
    return lista[1]

def centralidad_(grafo):
    cent = {}
    for v in grafo: cent[v] = 0
    for v in grafo:
        # hacia todos los demas vertices
        distancia, padre = dijkstra(grafo, v)
        cent_aux = {}
        for w in grafo: cent_aux[w] = 0
        lista = []
        filtrar_infinitos(distancia)
        for x in distancia:
            lista.append([x, distancia[x]])
        lista.sort(reverse=True, key=segundo_item)
        #print(lista)
        for w in lista:
            if w[0] == v: continue
            cent_aux[padre[w[0]]] += (1 + cent_aux[w[0]])
        # le sumamos 1 a la centralidad de todos los vertices que se encuentren en
        # el medio del camino
        for w in grafo:
            if w == v: continue
            cent[w] += cent_aux[w]

    return cent

def imprimir_resultado(camino, sep):
    for a in range(len(camino)-1):
        print(camino[a], end=sep)
    print(camino[len(camino)-1])

def cargar_ciudades_y_aeropuertos(archivo_1):
    archivo = open(archivo_1)
    ciudades = {}
    aeropuertos = {}
    for linea in archivo:
        linea = linea.replace('\n', '')
        separado = linea.split(",")
        if not separado[0] in ciudades:
            ciudades[separado[0]] = Ciudad()
        ciudades[separado[0]].agregar_aeropuerto(separado[1], separado[2], separado[3])
        aeropuertos[separado[1]] = [separado[2], separado[3]]
    archivo.close()
    return ciudades, aeropuertos

def clave_vuelo(aeropuerto1, aeropuerto2):
    return aeropuerto1 + "|" + aeropuerto2

def cargar_vuelos(archivo_2):
    archivo = open(archivo_2)
    vuelos = {}
    for linea in archivo:
        linea = linea.replace('\n', '')
        separado = linea.split(",")
        clave = clave_vuelo(separado[0], separado[1])
        vuelos[clave] = (separado[2], separado[3], separado[4])
    archivo.close()
    return vuelos

def armar_grafo(ciudades, vuelos, modo="rapido"):
    grafo = Grafo()
    indice = 0
    if modo == "barato": indice = 1


    for c in ciudades:
        for aeropuerto in ciudades[c]: grafo.agregar_vertice(aeropuerto)
    for v in vuelos:
        separado = v.split("|")
        if modo == "cantidad":
            grafo.agregar_arista(separado[0], separado[1], float(1/float(vuelos[v][2])))
            grafo.agregar_arista(separado[1], separado[0], float(1/float(vuelos[v][2])))
        else:
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

def dijkstra(grafo, origen, ciudad_destino=None):

    dist = {}
    padre = {}

    for v in grafo: dist[v] = math.inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap(comparacion)
    q.encolar([origen, dist[origen]])
    while not q.esta_vacia():
        v = q.desencolar()[0]
        if ciudad_destino:
            if v in ciudad_destino: return reconstruir_camino(origen, v, padre, dist)
        for w in grafo.adyacentes(v):
            if dist[v] + grafo.peso_union(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_union(v, w)
                padre[w] = v
                q.encolar([w, dist[w]])
    if not ciudad_destino: return dist, padre


def bfs(grafo, origen, destino=None):
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
                if destino:
                    if w in destino: return reconstruir_camino(origen, w, padres, orden)
                q.encolar(w)
    if not destino: return orden, padres


def cargar_archivo(archivo):
    """Carga los datos recibidos de itinerario.csv y devuelve una lista de las ciudades a visitar
    junto con un grafo de orden topologico"""
    grafo = Grafo()
    ciudades = []
    with open(archivo) as a:
        linea = a.readline().rstrip()
        separado = linea.split(",")
        for x in separado:
            ciudades.append(x)
            grafo.agregar_vertice(x)
        while True:
            linea = a.readline().rstrip()
            if not linea: break
            restriccion = linea.split(",")
            grafo.agregar_arista(restriccion[0], restriccion[1])
    return grafo, ciudades
    
def orden_topologico(grafo):
    """Algoritmo de orden topologico, devuelve una lista con el orden a realizar"""
    orden = {}
    resultado = []
    q = Cola()
    for v in grafo: orden[v] = 0
    for v in grafo:
        for w in grafo.adyacentes(v): orden[w] += 1
    for v in grafo:
        if orden[v] == 0: q.encolar(v)
    while not q.esta_vacia():
        v = q.desencolar()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            orden[w] -= 1
            if orden[w] == 0: q.encolar(w)
    return resultado
