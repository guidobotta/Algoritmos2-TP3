#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
from ciudad import *
#Modulos de Python
from operator import itemgetter
import sys
import random
import math

def filtrar_infinitos(distancia):
    """
    Recibe una lista con distancias y elimina aquellas que
    sean infinito.
    """
    for v in distancia:
        if distancia[v] == math.inf: distancia.pop(v)

def ordenar_vertices(distancia):
    """
    Los vertices se ordenan 'solos' al pasarlos a una lista.
    """
    lista = []
    for v in distancia:
        lista.insert(0, v)
    print(lista)
    return lista

def centralidad_(grafo):
    """

    """
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
    """
    Recibe un camino (elemento iterable), e imprime el
    resultado del camino con formato.
    """
    for elem in range(len(camino)-1):
        print(camino[elem], end=" -> ")
    print(camino[len(camino)-1])

def cargar_ciudades_y_aeropuertos(archivo):
    """
    Recibe un archivo csv con vuelos con el formato:
    'ciudad,codigo_aeropuerto,latitud,longitud'
    y devuelve dos diccionario con la información cargada, uno de
    ciudades y otro de aeropuertos.
    """
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

def cargar_vuelos(archivo):
    """
    Recibe un archivo csv con vuelos con el formato:
    'aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos'
    y devuelve un diccionario con la información cargada
    """
    vuelos = {}
    with open(archivo) as vuelos_csv:
        for linea in vuelos_csv:
            linea = linea.replace('\n', '')
            info_vuelo = linea.split(",")
            clave = info_vuelo[0] + "|" + info_vuelo[1]
            vuelos[clave] = (info_vuelo[2], info_vuelo[3], info_vuelo[4])
    return vuelos

def armar_grafo(ciudades, vuelos, modo):
    """
    Recibe un diccionario de ciudades y otro de vuelos, y el modo
    en el que debe ser creado.
    Devuelve un grafo con aeropuertos como vertices y el peso de las
    aristas según el modo.
    """
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
    """
    Compara dos elementos.
    """
    if x[1] < y[1]: return 1
    if x[1] > y[1]: return -1
    return 0

def reconstruir_camino(origen, destino, padre, distancia):
    """
    Recibe un vertice(origen), un vertice(destino), un diccionario
    de padres, y un diccionario con distancias.
    Devuelve el camino reconstruído y la distancia total.
    """
    resultado = []
    distancia_total = distancia[destino]
    while destino != origen:
        resultado.insert(0, destino)
        destino = padre[destino]
    resultado.insert(0, origen)
    return resultado, distancia_total

def dijkstra(grafo, origen, ciudad_destino):
    """
    Recibe un grafo, un vertice origen y un vertice destino y
    aplica el algoritmos de dijkstra para encontrar el camino mínimo.
    """
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
            if dist[v] + grafo.peso_arista(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_arista(v, w)
                padre[w] = v
                q.encolar([w, dist[w]])
    #Devolvemos algo acá?

def bfs(grafo, origen, destino):
    """
    Recibe un grafo, un vertice origen y un vertice destino y aplica bfs.
    """
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

def cargar_archivo(archivo):
    """Carga los datos recibidos de itinerario.csv y devuelve una lista de las ciudades a visitar
    junto con un grafo de orden topologico"""
    grafo = Grafo()
    with open(archivo) as a:
        linea = a.readline().rstrip()
        separado = linea.split(",")
        for x in separado:
            grafo.agregar_vertice(x)
        while True:
            linea = a.readline().rstrip()
            if not linea: break
            restriccion = linea.split(",")
            grafo.agregar_arista(restriccion[0], restriccion[1])
    return grafo

def orden_topologico(grafo):
    """Algoritmo de orden topologico, devuelve una lista con el orden a realizar"""
    orden = {}
    resultado = []
    q = Cola()

    for v in grafo: 
        orden[v] = 0

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

def comparacion_prim(tup_1, tup_2):
    """
    Recibe dos tuplas de la forma:
    (vertice1, vertice2, peso)
    Compara el peso entre ellos y devuelve:
    1 si tup_1 < tup_2
    0 si tup_1 == tup_2
    -1 si tup_1 > tup_2
    """
    peso_1 = tup_1[2]
    peso_2 = tup_2[2]
    if peso_1 < peso_2: return 1
    elif peso_1 == peso_2: return 0
    else: return -1

def prim(grafo, vertice):
    """
    Recibe un grafo y un vertice aleatorio de dicho grafo.
    Devuelve un arbol de tendido minimo(Grafo).
    """
    visitados = set()
    q = Heap(comparacion_prim)
    arbol = Grafo()

    visitados.add(vertice)
    for w in grafo.adyacentes(vertice):
        q.encolar((vertice, w, grafo.peso_arista(vertice, w)))
    for v in grafo.obtener_vertices():
        arbol.agregar_vertice(v)
    while not q.esta_vacia():
        (v,w, peso) = q.desencolar()
        if w in visitados:
            continue
        visitados.add(w)
        arbol.agregar_arista(v, w, peso)
        for x in grafo.adyacentes(w):
            if x not in visitados:
                q.encolar((w,x,grafo.peso_arista(w,x)))
    
    return arbol

def escribir_archivo(archivo, ab_min, vuelos):
    """
    Recibe una ruta a .csv, un grafo "arbol de tendido mínimo",
    y un diccionario con vuelos y su información.
    Escribe un archivo .csv a la ruta indicada.
    """
    visitados = set()
    with open(archivo, 'w') as arch:
        for v in ab_min:
            if v in visitados:
                continue
            aero_i = v 
            visitados.add(v)
            for w in ab_min.adyacentes(v):
                if w in visitados:
                    continue
                visitados.add(w)
                aero_j = w
                clave = aero_i + "|" + aero_j
                if clave not in vuelos:
                    clave = aero_j + "|" + aero_i
                tiempo_promedio = vuelos[clave][0]
                precio = vuelos[clave][1]
                cant_vuelos = vuelos[clave][2]
                arch.write("{},{},{},{},{}\n".format(aero_i, aero_j,\
                tiempo_promedio, precio, cant_vuelos))

def calc_prank(grafo):
    """
    Recibe un grafo de aeropuertos.
    Devuelve una lista ordenada de los mas importantes.
    """
    prank = {}
    for v in grafo:
        prank[v] = 0
    d = 0.85
    for i in range(20):
    #PODEMOS CAMBIAR EL FOR POR UNA CONDICION DE CONVERGENCIA
    #HABRIA QUE HACER UNA FUNCIÓN APARTE
        for v in grafo:
            prank_ady = 0
            for ady in grafo.adyacentes(v):
                prank_ady += (prank[ady]/len(grafo.adyacentes(ady)))
            prank[v] = ( ((1-d)/len(prank)) + (d*prank_ady) )
    lista = []
    for aero in prank:
        lista.append((aero, prank[aero]))
    lista.sort(key=itemgetter(1), reverse=True)
    return lista