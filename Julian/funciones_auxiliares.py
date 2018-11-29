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



def rec_recursivo(grafo, v, origen, resultado, visitados, d_actual, d_referencia, a_apariciones, aeropuertos, ciudades):
    numero = 0
    numero = a_apariciones[v]
    a_apariciones[v] = numero + 1
    ciudad = aeropuertos[v][0]
    visitados[ciudad] = True
    resultado.append(v)
    if len(visitados) == len(ciudades): return
    if a_apariciones[v] > 30: return
    #print(d_actual[0])
    if d_actual[0] < d_referencia:
        for w in grafo.adyacentes(v):
            d_actual[0] += grafo.peso_arista(v, w)
            rec_recursivo(grafo, w, v, resultado, visitados, d_actual, d_referencia, a_apariciones, aeropuertos, ciudades)
    else:
        resultado.pop()
        numero = a_apariciones[v]
        a_apariciones[v] = numero - 1
        eliminar = True
        for x in ciudades[ciudad]:
            if x[0] in a_apariciones:
                if a_apariciones[x[0]] != 0: eliminar = False
        if eliminar:
            visitados.pop(ciudad)
        if not origen: return
        d_actual[0] -= grafo.peso_arista(origen, v)
    return

def recorrer_recursivo(grafo, origen, aeropuertos, visitados, resultado, padres, ciudades, a_visitados):
    v = origen
    adyacentes = []
    resultado.append(v)
    #print(visitados)
    for w in grafo.adyacentes(v):
        adyacentes.append([w, grafo.peso_arista(v, w)])
    adyacentes.sort(key=segundo_item)
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
    distancia = 0
    for i in range(len(camino)-1):
        #print(i)
        distancia += grafo.peso_arista(camino[i], camino[i+1])
    return distancia


def vertice_aleatorio(pesos):
    #Pesos es un diccionario de pesos, clave vértice vecino, valor el peso.
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + peso_arista >= rand:
            return vertice
        acum += peso_arista

def random_walks(grafo, origen, apariciones, k):
    #Contador de apariciones de un vertice
    for a in range(k):
        pesos = {}
        for w in grafo.adyacentes(origen):
            pesos[w] = grafo.peso_arista(origen,w)
        origen = vertice_aleatorio(pesos)
        apariciones[origen] += 1



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
        aeropuertos[separado[1]] = [separado[0], separado[2], separado[3]]
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
    if modo == "barato":
        indice = 1
    elif modo == "cent_aprox":
        indice = 2


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
            if dist[v] + grafo.peso_arista(v, w) < dist[w]:
                dist[w] = dist[v] + grafo.peso_arista(v, w)
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
        arbol.agregar_arista(w, v, peso)
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
