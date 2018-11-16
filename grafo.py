class Grafo:
    """
    Clase Grafo implementada sobre lista de adyacencia
    con diccionario de diccionarios.
    """ #O diccionario de conjuntos

    def __init__(self):
        """Constructor de la clase grafo."""
        self.adyacentes = {}

    def añadir_vertice(self, vert):
        """Recibe un vertice y lo agrega."""
        self.adyacentes[vert] = None

    def añadir_arista(self, vert1, vert2):
        #Se puede hacer que recibe una tupla de dos vertices
        """"""
    
    def eliminar_vertice(self, vert):
        """Recibe un vertice y lo elimina."""

    def eliminar_arista(self, vert1, vert2):
        """"""

    def __iter__(self):
        return _Iter_Grafo_(self.adyacentes)

class _Iter_Grafo_:
    """
    Clase Iterador del Grafo.
    """

    def __init__(self, adyacentes):

        