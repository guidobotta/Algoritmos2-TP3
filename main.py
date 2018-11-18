#Modulos internos
from grafo import *
from heap import *
from cola import *
from pila import *
#Modulos de Python
import sys

_LISTA_OPERACIONES_ = ["camino_mas","camino_escalas","centralidad",\
"centralidad_aprox","pagerank","nueva_aerolinea","recorrer_mundo",\
"recorrer_mundo_aprox","vacaciones","itinerario_cultural","exportal_kml"]

def listar_operaciones():
    """Imprime una línea por cada comando implementado."""
    for operacion in _LISTA_OPERACIONES_:
        print(operacion)

def camino_mas(comando):
    """"""
    return

def camino_escalas(comando):
    """"""
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
    """"""
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

def exportal_kml(comando):
    """"""
    return

def ejecutar(linea):
    """Recibe una linea y ejecuta la operación correspondiente.
    En caso de no recibir una operación correcta, levanta un error."""
    comando = linea.split(' ')
    if (comando[0] == 'listar_operaciones'): listar_operaciones()
    elif (comando[0] == 'camino_mas'): camino_mas(comando)
    elif (comando[0] == 'camino_escalas'): camino_escalas(comando)
    elif (comando[0] == 'centralidad'): centralidad(comando)
    elif (comando[0] == 'centralidad_aprox'): centralidad_aprox(comando)
    elif (comando[0] == 'pagerank'): pagerank(comando)
    elif (comando[0] == 'nueva_aerolinea'): nueva_aerolinea(comando)
    elif (comando[0] == 'recorrer_mundo'): recorrer_mundo(comando)
    elif (comando[0] == 'recorrer_mundo_aprox'): recorrer_mundo_aprox(comando)
    elif (comando[0] == 'vacaciones'): vacaciones(comando)
    elif (comando[0] == 'itinerario_cultural'): itinerario_cultural(comando)
    elif (comando[0] == 'exportal_kml'): exportal_kml(comando)
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

    while True:
        linea = entrada.readline()
        if not linea:
            break
        linea = linea.replace('\n', '')
        ejecutar(linea)

main()