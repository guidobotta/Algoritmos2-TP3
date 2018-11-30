#Funciones auxiliares
from funciones_auxiliares import *
import pdb

###
#   CONSTANTES GLOBLALES
###

_ULTIMA_RUTA_ = [[]]

_LISTA_OPERACIONES_ = ["camino_mas","camino_escalas","centralidad",\
"centralidad_aprox","pagerank","nueva_aerolinea","recorrer_mundo",\
"recorrer_mundo_aprox","vacaciones","itinerario_cultural","exportal_kml"]

###
#   FUNCIONES
###

def listar_operaciones():
    """
    Imprime una línea por cada comando implementado.
    """
    for operacion in _LISTA_OPERACIONES_:
        print(operacion)

def camino_mas(comando, ciudades, vuelos):
    """
    Imprime una lista con los aeropuertos (código) con los cuales vamos
    de la ciudad origen a la ciudad destino de la forma más rápida o más
    barata, según corresponda. Tener en cuenta que tanto la ciudad origen
    como la destino pueden tener más de un aeropuerto, y nos interesa la
    mejor forma (rápida o barata) entre todas las combinaciones posibles.

    Recibe una linea de comandos de la siguiente forma:
    "modo,ciudad_origen,ciudad_destino"
    El modo puede ser "rapido" o "barato".

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    linea = comando.split(",")

    modo = linea[0]
    grafo = armar_grafo(ciudades, vuelos, modo)

    ciudad_origen = ciudades[linea[1]].ver_aeropuertos()
    ciudad_destino = ciudades[linea[2]].ver_aeropuertos()
    mejor_distancia = math.inf
    for v in ciudad_origen:
        camino, distancia = dijkstra(grafo, v, ciudad_destino)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia

    imprimir_resultado(mejor_camino, " -> ")

    _ULTIMA_RUTA_[0] = mejor_camino

def camino_escalas(comando, ciudades, vuelos):
    """
    Imprime una lista con los aeropuertos (código) con los cuales vamos
    de la ciudad origen a la ciudad destino con la menor cantidad de
    escalas.

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen,ciudad_destino"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    linea = comando.split(",")
    #Da igual que peso le damos a las aristas
    grafo = armar_grafo(ciudades, vuelos, "rapido")

    ciudad_origen = ciudades[linea[0]].ver_aeropuertos()
    ciudad_destino = ciudades[linea[1]].ver_aeropuertos()

    mejor_distancia = math.inf
    for v in ciudad_origen:
        camino, distancia = bfs(grafo, v, ciudad_destino)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia
    imprimir_resultado(mejor_camino, " -> ")
    _ULTIMA_RUTA_[0] = mejor_camino

def centralidad(comando, ciudades, vuelos):
    """
    Muestra los n aeropuertos más centrales/importantes del mundo, de
    mayor importancia a menor importancia.

    Recibe una linea de comandos de la siguiente forma:
    "cantidad_aeropuertos_a_mostrar"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    n = int(comando)
    grafo = armar_grafo(ciudades, vuelos, "vuelos")
    lista = []
    resultado = []
    centrales = centralidad_(grafo)
    for a in centrales:
        lista.append([a, centrales[a]])
    lista.sort(reverse=True, key=segundo_item)
    for i in lista:
        if n < 1: break
        resultado.append(i[0])
        n -= 1

    imprimir_resultado(resultado, ", ")
    return

def centralidad_aprox(comando, ciudades, vuelos):
    """
    Nuestra los n aeropuertos más centrales/importantes del mundo de
    forma aproximada, de mayor importancia a menor importancia.

    Recibe una linea de comandos de la siguiente forma:
    "cantidad_aeropuertos_a_mostrar"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    grafo = armar_grafo(ciudades, vuelos, "cent_aprox")
    origen = grafo.vertice_aleatorio()
    k=20
    apariciones = {}
    lista = []
    resultado = []
    n = int(comando)
    for v in grafo:
        apariciones[v] = 0
    random_walks(grafo, origen, apariciones, k)
    for x in apariciones:
        lista.append([x, apariciones[x]])
    lista.sort(reverse=True, key=segundo_item)
    for i in lista:
        if n < 1: break
        resultado.append(i[0])
        n -= 1

    imprimir_resultado(resultado, ", ")
    #Crear un grafo con cantidad de vuelos como peso
    #Elegir un vertice vertice aleatorio
    #Llamar a Random_Walks para ese vertice
    #Realizar este ciclo K veces
    #Devolver la lista generada
    return

def pagerank(comando, ciudades, vuelos):
    """
    Muestra los n aeropuertos más centrales/importantes del mundo según
    el algoritmo de pagerank, de mayor importancia a menor importancia.

    Recibe una linea de comandos de la siguiente forma:
    "cantidad_aeropuertos_a_mostrar"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    grafo = armar_grafo(ciudades, vuelos, "rapido")
    cantidad = int(comando)
    lista_aeropuertos = calc_prank(grafo)
    for i in range(cantidad-1):
        print(lista_aeropuertos[i][0], end=",")
    print(lista_aeropuertos[cantidad-1][0])

def nueva_aerolinea(comando, ciudades, vuelos):
    """
    Crea un archivo .csv con las rutas que permitan implementar una nueva
    aerolínea tal que se pueda comunicar a todos los aeropuertos con
    dicha aerolínea, pero que el costo total de la licitación de las
    rutas aéreas sea mínima.

    El formato del archivo creado será de la forma:
    'aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos'.

    Recibe una linea de comandos de la siguiente forma:
    "ruta_archivo_de_salida.csv"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    archivo = comando
    grafo = armar_grafo(ciudades, vuelos, "barato")
    ab_min = prim(grafo, grafo.obtener_vertice_aleatorio())
    escribir_archivo(archivo, ab_min, vuelos)

def recorrer_mundo(comando, ciudades, vuelos, aeropuertos):
    """
    Devuelve una lista en orden de cómo debemos movernos por el mundo
    para visitar todas las ciudades del mundo, demorando lo menos posible.

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    grafo = armar_grafo(ciudades, vuelos, "rapido")
    origen = comando

    visitados = {}
    for ciudad in ciudades:
        visitados[ciudad] = 0
    visitados[origen] = 1

    peso_minimo = obtener_minimo(grafo)
    solucion = [[]]
    dist_actual = [0]
    dist_referencia = [0]
    aeros_ciudad = ciudades[origen].ver_aeropuertos()
    mejor_camino, dist_referencia[0] = recorrer_mundo_aprox(origen, ciudades, vuelos, aeropuertos)

    for aero_origen in aeros_ciudad:
        n = [0]
        recorrido = [aero_origen]
        rec_recursivo(grafo, aero_origen, aeropuertos, visitados, recorrido, dist_actual, dist_referencia, solucion,peso_minimo,n)

    print(solucion[0])

def recorrer_mundo_aprox(comando, ciudades, vuelos, aeropuertos):
    """
    Devuelve una lista en orden de cómo debemos movernos por el mundo
    para visitar todas las ciudades del mundo, demorando aproximadamente
    lo menos posible.

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
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
    arbol = prim(grafo, aeropuerto_origen)
    recorrer_recursivo(arbol, aeropuerto_origen, aeropuertos, visitados, resultado, padres, ciudades, a_visitados)

    #imprimir_resultado(resultado, " -> ")
    """
    for i in range(len(resultado)-1):
        try:
             grafo.peso_arista(resultado[i], resultado[i+1])
        except:
            print("Hubo problemas conectando estos aeropuertos: ")
            print(resultado[i] + ", " + resultado[i+1])
            problemas.append(resultado[i-2])
            problemas.append(resultado[i-1])
            problemas.append(resultado[i])
            problemas.append(resultado[i+1])
            break
    for v in problemas:
        print(v, end=": ")
        for w in grafo.adyacentes(v):
            print(w, end=", ")
        print("\n")
    chequeo = []
    for x in resultado:
        chequeo.append(aeropuertos[x][0])
    for a in ciudades:
        if a not in chequeo: print(a)
    """
    distancia = reconstruir_distancia(arbol, resultado)
    #print(distancia)
    return resultado, distancia


def vacaciones(comando, ciudades, vuelos):
    """
    Devuelve algún recorrido que comience en origen y que termine en origen
    también, de largo n (sin contar la última vuelta al origen).
    No debe pasarse por un aeropuerto más de una vez (salvo el origen,
    cuando volvemos a éste). En caso de no encontrar un recorrido de dicho
    largo que vuelva luego al origen, imprime "No se encontro recorrido"

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen,cantidad_ciudades_a_visitar"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    comandos = comando.split(",")
    lista_aeropuertos = ciudades[comandos[0]].ver_aeropuertos()
    for ind_aero in range(len(lista_aeropuertos)):
        #Pruebo a partir de cada uno de los aeropuertos de la ciudad
        comandos = comando.split(',')
        grafo = armar_grafo(ciudades,vuelos, "rapido")
        origen = lista_aeropuertos[ind_aero]
        cantidad = int(comandos[1])
        recorrido = [origen]

        if vacaciones_aux(origen, origen, grafo, recorrido, cantidad):
            recorrido.append(origen)
            imprimir_resultado(recorrido, " -> ")
            return

    print("No se encontró recorrido")

def itinerario_cultural(comando, ciudades, vuelos):
    """
    Recibe una linea de comandos de la siguiente forma:
    "ruta_archivo.csv"
    El archivo de ruta tiene el formato:
    "
    ciudad_1,ciudad_2,ciudad_3, ...,ciudad_N
    ciudad_i,ciudad_j
    ...
    "
    La primera línea indica las ciudades que se desean visitar. Las
    siguientes indican que la ciudad_i debe visitarse sí o sí antes que
    la ciudad_j.

    Imprime el orden en el que deben visitarse dichas ciudades y el camino
    mínimo en tiempo a realizar.

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    grafo = cargar_archivo(comando)
    orden = orden_topologico(grafo)
    imprimir_resultado(orden, ", ")
    for i in range(len(orden)-1):
        camino_mas("rapido,"+ orden[i] + "," + orden[i+1], ciudades, vuelos)

def exportar_kml(comando, aeropuertos):
    """
    Exporta la ruta del último comando ejecutado a un archivo KML.
    """
    ruta = _ULTIMA_RUTA_[0]
    encabezado = \
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    declaracion = "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n\
        <Document>"
    nombre = "\t\t<name>Ruta de vuelo</name>"

    abrir_punto1 = "\t\t<Placemark>\n\
                    <name>"
    abrir_punto2 =  "\t\t    </name>\n\
                    <Point>\n\
                        <coordinates>"
    cerrar_punto = "\t\t\t</coordinates>\n\
                    </Point>\n\
                </Placemark>"

    abrir_linea = "\t\t<Placemark>\n\
                    <LineString>\n\
                        <coordinates>"

    cerrar_linea =  "\t\t\t</coordinates>\n\
                    </LineString>\n\
                </Placemark>"

    cerrar_documento = "\t</Document>\n\
    </kml>"
    with open(comando, 'w') as f:
        f.write(encabezado + "\n")
        f.write(declaracion + "\n")
        f.write(nombre + "\n")
        for aeropuerto in ruta:
            f.write(abrir_punto1 + "\n")
            f.write("\t\t\t" + aeropuerto + "\n")
            f.write(abrir_punto2 + "\n")
            f.write("\t\t\t\t" + str(aeropuertos[aeropuerto][1]) + ", " + str(aeropuertos[aeropuerto][2]) + "\n")
            f.write(cerrar_punto + "\n")
        anterior = None
        for aeropuerto in ruta:
            if not anterior:
                anterior = aeropuerto
                continue
            f.write(abrir_linea + "\n")
            f.write("\t\t\t\t" + str(aeropuertos[anterior][1]) + ", " + str(aeropuertos[anterior][2]) + " " + str(aeropuertos[aeropuerto][1]) + ", " + str(aeropuertos[aeropuerto][2]) + "\n")
            f.write(cerrar_linea + "\n")
        #linea
        f.write(cerrar_documento + "\n")

###
#   EJECUTADOR
###

from time import time

def ejecutar(linea, ciudades, vuelos, aeropuertos):
    """
    Recibe una linea y ejecuta la operación correspondiente.
    En caso de no recibir una operación correcta, levanta un error.
    """
    comando = linea.split(' ', 1)

    tiempo = time()
    if (comando[0] == 'listar_operaciones'): listar_operaciones()
    elif (comando[0] == 'camino_mas'): camino_mas(comando[1], ciudades, vuelos)
    elif (comando[0] == 'camino_escalas'): camino_escalas(comando[1], ciudades, vuelos)
    elif (comando[0] == 'centralidad'): centralidad(comando[1], ciudades, vuelos)
    elif (comando[0] == 'centralidad_aprox'): centralidad_aprox(comando[1], ciudades, vuelos)
    elif (comando[0] == 'pagerank'): pagerank(comando[1], ciudades, vuelos)
    elif (comando[0] == 'nueva_aerolinea'): nueva_aerolinea(comando[1], ciudades, vuelos)
    elif (comando[0] == 'recorrer_mundo'): recorrer_mundo(comando[1], ciudades, vuelos, aeropuertos)
    elif (comando[0] == 'recorrer_mundo_aprox'): recorrer_mundo_aprox(comando[1], ciudades, vuelos, aeropuertos)
    elif (comando[0] == 'vacaciones'): vacaciones(comando[1], ciudades, vuelos)
    elif (comando[0] == 'itinerario'): itinerario_cultural(comando[1], ciudades, vuelos)
    elif (comando[0] == 'exportar_kml'): exportar_kml(comando[1], aeropuertos)
    print(f"Tardo: {time()-tiempo}seg")


###
#   MAIN
###

def main():
    """
    Ejecuta el cuerpo principal del programa.

    Al ejecutarse, se deben pasar dos parámetros extra. Un archivo csv con
    aeropuertos con el formato 'ciudad,codigo_aeropuerto,latitud,longitud'.
    Y otro archivo csv con vuelos con el formato
    'aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos'.
    En caso de no pasar estos parámetros, se levantará un error y terminará el programa.

    Se leerán las lineas de la entrada estandar para ejecutar las operaciones.
    El programa contará con distintas operaciones que se podrán obtener ejecutando el
    comando listar_operaciones.
    """
    if (len(sys.argv) != 3):
        print("Error en cantidad de parámetros. Se esperaban 3 y se recibieron {}"\
        .format(len(sys.argv)), file=sys.__stderr__)
        return

    archivo_1 = sys.argv[1]
    archivo_2 = sys.argv[2]

    entrada = sys.__stdin__

    ciudades, aeropuertos = cargar_ciudades_y_aeropuertos(archivo_1)
    vuelos = cargar_vuelos(archivo_2)
    if not ciudades or not vuelos: raise Exception("Fallo al cargar archivos")

    while True:
        linea = entrada.readline()
        if not linea:
            break
        linea = linea.replace('\n', '')
        ejecutar(linea, ciudades, vuelos, aeropuertos)

main()
