#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
from ciudad import *
#Modulos de Python
from operator import itemgetter
import sys
import math
import random

###
#   MAIN FUNCTIONS
###

def cargar_ciudades_y_aeropuertos(archivo_1):
    """
    Recibe un archivo csv con vuelos con el formato:
    'ciudad,codigo_aeropuerto,latitud,longitud'
    y devuelve dos diccionario con la información cargada, uno de
    ciudades y otro de aeropuertos.
    """
    archivo = open(archivo_1)
    ciudades = {}
    aeropuertos = {}
    for linea in archivo:
        linea = linea.replace('\n', '')
        separado = linea.split(",")
        if not separado[0] in ciudades:
            ciudades[separado[0]] = Ciudad()
        ciudades[separado[0]].agregar_aeropuerto(separado[1], separado[2], separado[3])
        aeropuertos[separado[1]] = [separado[0], separado[2], separado[3]]
    archivo.close()
    return ciudades, aeropuertos

def clave_vuelo(aeropuerto1, aeropuerto2):
    """
    Genera la clave vuelo y la devuelve.
    Recibe dos aeropuertos (strings).
    """
    return aeropuerto1 + "|" + aeropuerto2

def cargar_vuelos(archivo_2):
    """
    Recibe un archivo csv con vuelos con el formato:
    'aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos'
    y devuelve un diccionario con la información cargada
    """
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
    """
    Recibe un diccionario de ciudades y otro de vuelos, y el modo
    en el que debe ser creado.
    Devuelve un grafo con aeropuertos como vertices y el peso de las
    aristas según el modo.
    """
    grafo = Grafo()
    indice = 0
    if modo == "barato": indice = 1

    for c in ciudades:
        for aeropuerto in ciudades[c]: grafo.agregar_vertice(aeropuerto)
    for v in vuelos:
        separado = v.split("|")
        if modo == "cantidad":
            grafo.agregar_arista(separado[0], separado[1], (1/float(vuelos[v][2])))
            grafo.agregar_arista(separado[1], separado[0], (1/float(vuelos[v][2])))
        else:
            grafo.agregar_arista(separado[0], separado[1], int(vuelos[v][indice]))
            grafo.agregar_arista(separado[1], separado[0], int(vuelos[v][indice]))
    return grafo

def imprimir_resultado(camino, sep):
    """
    Recibe un camino (elemento iterable), e imprime el
    resultado del camino con formato.
    """
    for a in range(len(camino)-1):
        print(camino[a], end=sep)
    print(camino[len(camino)-1])

###
#   DIJKSTRA (camino_mas)
###

def comparacion_dijkstra(x, y):
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

def dijkstra(grafo, origen, ciudad_destino=None):
    """
    Recibe un grafo, un vertice origen y un vertice destino y
    aplica el algoritmos de dijkstra para encontrar el camino mínimo.
    """
    dist = {}
    padre = {}

    for v in grafo: dist[v] = math.inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap(comparacion_dijkstra)
    q.encolar([origen, dist[origen]])
    while not q.esta_vacia():
        v = q.desencolar()[0]
        if ciudad_destino:
            if v in ciudad_destino: return reconstruir_camino(origen, v, padre, dist)
        for w in grafo.adyacentes(v):
            if dist[v] + grafo.peso_arista(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_arista(v, w)
                padre[w] = v
                q.encolar([w, dist[w]])
    if not ciudad_destino: return dist, padre

###
#   BFS (camino_escalas)
###

def bfs(grafo, origen, destino=None):
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
                if destino:
                    if w in destino: return reconstruir_camino(origen, w, padres, orden)
                q.encolar(w)
    if not destino: return orden, padres

###
#   Centralidad
###

def filtrar_infinitos(distancia):
    """
    Recibe una lista con distancias y elimina aquellas que
    sean infinito.
    """
    for v in distancia:
        if distancia[v] == math.inf: distancia.pop(v)

def centralidad_aux(grafo):
    """
    Recibe un grafo y calcula la centralidad de los aeropuertos.
    """
    cent = {}
    for v in grafo: cent[v] = 0

    for v in grafo:
        distancia, padre = dijkstra(grafo, v)
        cent_aux = {}
        
        for w in grafo: cent_aux[w] = 0
        lista = []
        filtrar_infinitos(distancia)

        for x in distancia:
            lista.append([x, distancia[x]])
        lista.sort(reverse=True, key=itemgetter(1))

        for w in lista:
            if w[0] == v: continue
            cent_aux[padre[w[0]]] += (1 + cent_aux[w[0]])

        for w in grafo:
            if w == v: continue
            cent[w] += cent_aux[w]

    return cent

###
#   Centralidad Aproximada
###

def random_walks(grafo, origen, apariciones, k):
    """
    Recibe un grafo, un vertice de origen, un diccionario de apariciones y
    un número k, que es la cantidad de veces que debe aplicarse random_walks
    para converger.
    """
    #Contador de apariciones de un vertice
    for a in range(k):
        pesos = {}
        for w in grafo.adyacentes(origen):
            pesos[w] = grafo.peso_arista(origen,w)
        origen = vertice_aleatorio(pesos)
        apariciones[origen] += 1

def vertice_aleatorio(pesos):
    """
    Recibe un diccionario de pesos de la forma {vertice vecino: peso}.
    Devuelve un vertice aleatorio.
    """
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + peso_arista >= rand:
            return vertice
        acum += peso_arista

###
#   Pagerank
###

def calc_prank(grafo, k, cantidad):
    """
    Recibe un grafo de aeropuertos, un número 'k', que es la cantidad de
    veces que es necesario aplicar pagerank para que converja, y un
    número 'cantidad', que es la cantidad de aeropuertos a mostrar.
    Devuelve una lista ordenada de los 'cantidad' aeropuertos mas 
    importantes.
    """
    prank = {}
    for v in grafo:
        prank[v] = 0
    d = 0.85
    for i in range(k):
        for v in grafo:
            prank_ady = 0
            for ady in grafo.adyacentes(v):
                prank_ady += (prank[ady]/len(grafo.adyacentes(ady)))
            prank[v] = ( ((1-d)/len(prank)) + (d*prank_ady) )
    lista = []
    for aero in prank:
        lista.append((aero, prank[aero]))
    lista.sort(key=itemgetter(1), reverse=True)
    resultado = []
    for i in range(cantidad):
        resultado.append(lista[i][0])
    return resultado

###
#   Nueva Aerolinea
###

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

def prim(grafo, vertice, no_dir):
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
        if no_dir: arbol.agregar_arista(w, v, peso)
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
            aero_i = v
            for w in ab_min.adyacentes(v):
                aero_j = w
                clave = aero_i + "|" + aero_j
                if clave not in vuelos:
                    clave = aero_j + "|" + aero_i
                visitados.add(clave)
                tiempo_promedio = vuelos[clave][0]
                precio = vuelos[clave][1]
                cant_vuelos = vuelos[clave][2]
                arch.write("{},{},{},{},{}\n".format(aero_i, aero_j,\
                tiempo_promedio, precio, cant_vuelos))

###
#   Recorrer Mundo
###

def todos_visitados(visitados):
    """
    Recibe un diccionario de visitados de la forma {ciudad: numero}.
    Devuelve True si están todos visitados (distinto de 0), o False
    en caso contrario.
    """
    for city in visitados:
        if visitados[city] == 0:
            return False
    return True

def sin_visitar(visitados):
    """
    Recibe un diccionario de visitados de la forma {ciudad: numero}.
    Devuelve la cantidad de ciudades no visitadas (numero == 0).
    """
    n = 0
    for city in visitados:
        if visitados[city] == 0:
            n+=1
    return n

def obtener_minimo(grafo):
    """
    Recibe un grafo y devuelve el peso mínimo entre sus aristas.
    """
    aristas = grafo.aristas()
    peso = math.inf
    for arista in aristas:
        for vertice in arista:
            if arista[vertice] < peso:
                peso = arista[vertice]
    return peso

def rec_recursivo(grafo, vertice, aeropuertos, visitados, recorrido, dist_actual, dist_referencia, solucion, peso_minimo):
    """
    Recibe un grafo, un vertice, un diccionario de aeropuertos, un diccionario
    de visitados, una lista que irá obteniendo el recorrido, la distancia
    actual, la distancia de referencia(el tope), una lista solucion que será
    la solución definitiva, y el peso minimo del grafo.
    """
    if todos_visitados(visitados):
        if dist_actual[0] > dist_referencia[0]:
            return False
        else:
            dist_referencia[0] = dist_actual[0]
            solucion[0] = recorrido[:]

    if (dist_actual[0] + peso_minimo*sin_visitar(visitados)) > dist_referencia[0]:
        return False

    for ady in grafo.adyacentes(vertice):
        if (len(recorrido) > 4) and ((ady == recorrido[-2]) and (vertice == recorrido[-3])):
            continue
        recorrido.append(ady)
        visitados[aeropuertos[ady][0]] += 1
        dist_actual[0] += grafo.peso_arista(vertice, ady)
        if not rec_recursivo(grafo, ady, aeropuertos, visitados, recorrido, dist_actual, dist_referencia, solucion, peso_minimo):
            recorrido.pop()
            visitados[aeropuertos[ady][0]] -= 1
            dist_actual[0] -= grafo.peso_arista(vertice, ady)

###
#   Recorrer Mundo Aproximado
###

def recorrer_recursivo(grafo, origen, aeropuertos, visitados, resultado, padres, ciudades, a_visitados):
    """
    Recibe un grafo, un vértice de origen, un diccionario de aeropuertos,
    un diccionario de visitados, una lista resultado, un diccionario de
    padres, un diccionario de ciudades, y un diccionario de aeropuertos
    visitados.
    """
    v = origen
    adyacentes = []
    resultado.append(v)
    #print(visitados)
    for w in grafo.adyacentes(v):
        adyacentes.append([w, grafo.peso_arista(v, w)])
    adyacentes.sort(key=itemgetter(1))
    for i in adyacentes:
        if aeropuertos[i[0]][0] not in visitados:
            padres[i[0]] = v
            visitados[aeropuertos[i[0]][0]] = True
            a_visitados[i[0]] = True
            recorrer_recursivo(grafo, i[0], aeropuertos, visitados, resultado, padres, ciudades, a_visitados)
            if len(visitados) < len(ciudades): resultado.append(v)

    if len(visitados) < len(ciudades):
        for w in adyacentes:
            aeropuerto = w[0]
            if aeropuerto in a_visitados: continue
            #resultado.append(aeropuerto)
            padres[aeropuerto] = v
            a_visitados[aeropuerto] = True
            recorrer_recursivo(grafo, aeropuerto, aeropuertos, visitados, resultado, padres, ciudades, a_visitados)
            if len(visitados) < len(ciudades): resultado.append(v)

    return

def reconstruir_distancia(grafo, camino):
    """
    A partir de una lista que representa un camino de vertices reconstruye 
    la distancia recorrida.
    """
    distancia = 0
    for i in range(len(camino)-1):
        distancia += grafo.peso_arista(camino[i], camino[i+1])
    return distancia

def recorrer_mundo_aprox_aux(comando, ciudades, vuelos, aeropuertos):
    """
    Función auxiliar de recorrer_mundo_aprox.
    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen"
    También recibe tres diccionarios con la informacion de las ciudades,
    los vuelos y los aeropuertos.
    """
    grafo = armar_grafo(ciudades, vuelos, "rapido")
    ciudad_origen = comando
    visitados = {}
    a_visitados = {}
    resultado = []
    padres = {}
    aeropuertos_ciudad = ciudades[ciudad_origen].ver_aeropuertos()
    distancia_inicial = math.inf

    for v in aeropuertos_ciudad:
        for w in grafo.adyacentes(v):
            if grafo.peso_arista(v, w) < distancia_inicial:
                distancia_inicial = grafo.peso_arista(v, w)
                aeropuerto_origen = v

    visitados[aeropuertos[aeropuerto_origen][0]] = True
    padres[aeropuerto_origen] = None
    arbol = prim(grafo, aeropuerto_origen, True)
    recorrer_recursivo(arbol, aeropuerto_origen, aeropuertos, visitados, resultado, padres, ciudades, a_visitados)
    distancia = reconstruir_distancia(arbol, resultado)
    return resultado, distancia

###
#   Vacaciones
###

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

###
#   Itinerario Cultural
###

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

##################################################################################
