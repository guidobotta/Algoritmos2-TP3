#Funciones auxiliares
from funciones_auxiliares import *

_ULTIMA_RUTA_ = [[]]

_LISTA_OPERACIONES_ = ["camino_mas","camino_escalas","centralidad",\
"centralidad_aprox","pagerank","nueva_aerolinea","recorrer_mundo",\
"recorrer_mundo_aprox","vacaciones","itinerario_cultural","exportal_kml"]

def listar_operaciones():
    """Imprime una línea por cada comando implementado."""
    for operacion in _LISTA_OPERACIONES_:
        print(operacion)

def camino_mas(comando, ciudades, vuelos):
    """
    Recibe una linea de comandos de la siguiente forma:
    "modo,ciudad_orignen,ciudad_destino"
    El modo puede ser "rapido" o "barato".
    También recibe dos diccionarios con la informacion de las
    ciudades y los vuelos.
    """
    linea = comando.split(",")

    grafo = armar_grafo(ciudades, vuelos, linea[0])

    ciudad_origen = ciudades[linea[1]].ver_aeropuertos()
    ciudad_destino = ciudades[linea[2]].ver_aeropuertos()

    mejor_distancia = math.inf
    for v in ciudad_origen:
        camino, distancia = dijkstra(grafo, v, ciudad_destino)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia

    imprimir_resultado(mejor_camino)

    _ULTIMA_RUTA_[0] = mejor_camino
    return

def camino_escalas(comando, ciudades, vuelos):
    """
    
    """
    linea = comando.split(",")
    #Da igual que peso le damos a las aristas
    grafo = armar_grafo(ciudades, vuelos, linea[0])

    ciudad_origen = ciudades[linea[0]].ver_aeropuertos()
    ciudad_destino = ciudades[linea[1]].ver_aeropuertos()
    #Es solo para debuguear
    print(ciudad_origen)
    print(ciudad_destino)

    mejor_distancia = math.inf
    for v in ciudad_origen:
        camino, distancia = bfs(grafo, v, ciudad_destino)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia
    print("Camino encontrado: ")
    imprimir_resultado(mejor_camino)
    _ULTIMA_RUTA_[0] = mejor_camino
    return

def centralidad(comando):
    """"""
    return

def centralidad_aprox(comando):
    """"""
    return

def pagerank(comando):
    """"""
    return

def nueva_aerolinea(comando):
    """"""
    return

def recorrer_mundo(comando):
    """
    Devuelve una lista en orden de cómo debemos movernos por el mundo 
    para visitar todas las ciudades del mundo, demorando lo menos posible.
    """
    
    return

def recorrer_mundo_aprox(comando):
    """"""
    return

def vacaciones(comando):
    """"""
    return

def itinerario_cultural(comando):
    """"""
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

def ejecutar(linea, ciudades, vuelos, aeropuertos):
    """
    Recibe una linea y ejecuta la operación correspondiente.
    En caso de no recibir una operación correcta, levanta un error.
    """
    comando = linea.split(' ', 1)
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
    elif (comando[0] == 'itinerario_cultural'): itinerario_cultural(comando[1], ciudades, vuelos)
    elif (comando[0] == 'exportar_kml'): exportar_kml(comando[1], aeropuertos)
    else: print("Error")


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
    if not ciudades or not vuelos: return False
    #Imprimir las ciudades y vuelos para debuguear
    """
    for v in ciudades:
        print(v + ":" + str(ciudades[v].ver_aeropuertos()))
    print("/" * 50)

    for x in vuelos:
        print(x + ":" + str(vuelos[x]))

    print("/" * 50)
    """
    while True:
        linea = entrada.readline()
        if not linea:
            break
        linea = linea.replace('\n', '')
        ejecutar(linea, ciudades, vuelos, aeropuertos)
main()
