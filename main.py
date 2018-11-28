#Funciones auxiliares
from funciones_auxiliares import *

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
    return

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
    return

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
    return

def nueva_aerolinea(comando, ciudades, vuelos):
    """

    """
    return

def recorrer_mundo(comando, ciudades, vuelos):
    """
    Devuelve una lista en orden de cómo debemos movernos por el mundo
    para visitar todas las ciudades del mundo, demorando lo menos posible.

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    grafo = armar_grafo(ciudades, vuelos, "rapido")

    return

def recorrer_mundo_aprox(comando, ciudades, vuelos):
    """
    Devuelve una lista en orden de cómo debemos movernos por el mundo
    para visitar todas las ciudades del mundo, demorando aproximadamente
    lo menos posible.

    Recibe una linea de comandos de la siguiente forma:
    "ciudad_origen"

    También recibe dos diccionarios con la informacion de las ciudades y
    los vuelos.
    """
    return

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
    comandos = comando.split(',')
    grafo = armar_grafo(ciudades,vuelos, "rapido")
    origen = random.choice(ciudades[comandos[0]].ver_aeropuertos())
    cantidad = int(comandos[1])
    recorrido = [origen]

    if vacaciones_aux(origen, origen, grafo, recorrido, cantidad):
        recorrido.append(origen)
        imprimir_resultado(recorrido, " -> ")
    else:
        print("No se encontró recorrido")

def itinerario_cultural(comando, ciudades, vuelos):
    """Calcula el itinerario a partir de dos grafos, uno de ciudades con prioridad y otro de aeropuertos"""
    grafo, ciudades_a_visitar = cargar_archivo(comando)
    orden = orden_topologico(grafo)
    imprimir_resultado(orden, ", ")
    for i in range(len(ciudades_a_visitar)-1):
        camino_mas("rapido,"+ ciudades_a_visitar[i] + "," + ciudades_a_visitar[i+1], ciudades, vuelos)
    return

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
            f.write("\t\t\t\t" + str(aeropuertos[aeropuerto][0]) + ", " + str(aeropuertos[aeropuerto][1]) + "\n")
            f.write(cerrar_punto + "\n")
        anterior = None
        for aeropuerto in ruta:
            if not anterior:
                anterior = aeropuerto
                continue
            f.write(abrir_linea + "\n")
            f.write("\t\t\t\t" + str(aeropuertos[anterior][0]) + ", " + str(aeropuertos[anterior][1]) + " " + str(aeropuertos[aeropuerto][0]) + ", " + str(aeropuertos[aeropuerto][1]) + "\n")
            f.write(cerrar_linea + "\n")
        #linea
        f.write(cerrar_documento + "\n")

###
#   EJECUTADOR
###

def ejecutar(linea, ciudades, vuelos, aeropuertos):
    """
    Recibe una linea y ejecuta la operación correspondiente.
    En caso de no recibir una operación correcta, levanta un error.
    """
    comando = linea.split(' ', 1)
    try:
        if (comando[0] == 'listar_operaciones'): listar_operaciones()
        elif (comando[0] == 'camino_mas'): camino_mas(comando[1], ciudades, vuelos)
        elif (comando[0] == 'camino_escalas'): camino_escalas(comando[1], ciudades, vuelos)
        elif (comando[0] == 'centralidad'): centralidad(comando[1], ciudades, vuelos)
        elif (comando[0] == 'centralidad_aprox'): centralidad_aprox(ccomando[1], ciudades, vuelos)
        elif (comando[0] == 'pagerank'): pagerank(comando[1], ciudades, vuelos)
        elif (comando[0] == 'nueva_aerolinea'): nueva_aerolinea(comando[1], ciudades, vuelos)
        elif (comando[0] == 'recorrer_mundo'): recorrer_mundo(comando[1], ciudades, vuelos)
        elif (comando[0] == 'recorrer_mundo_aprox'): recorrer_mundo_aprox(comando[1], ciudades, vuelos)
        elif (comando[0] == 'vacaciones'): vacaciones(comando[1], ciudades, vuelos)
        elif (comando[0] == 'itinerario'): itinerario_cultural(comando[1], ciudades, vuelos)
        elif (comando[0] == 'exportar_kml'): exportar_kml(comando[1], aeropuertos)
    except:
        print("Error en comando {}".format(comando[0]))

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
