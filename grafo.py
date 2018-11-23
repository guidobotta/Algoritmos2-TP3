class Vertice:

    def __init__(self, nombre):
        """Constructor de la clase grafo."""
        self.adyacentes = {}

    def agregar(self, nombre, peso):
        """Añade un nuevo vertice a los adyacentes junto al peso de la union"""
        self.adyacentes[nombre] = peso

    def adyacentes_vertice(self):
        """Devuelve un diccionario con los adyacentes al vertice"""
        return self.adyacentes

    def union(self, nombre):
        """Devuelve el peso de la union entre el vertice A y B"""
        return self.adyacentes[nombre]

    def eliminar(self, nombre):
        """Elimina el vertice del diccionario de adyacentes del actual, en caso de existir"""
        if nombre in self.adyacentes:
            self.adyacentes.pop(nombre)

    def __str__(self):
        return str(self.adyacentes)

class Grafo:
    """
    Clase Grafo implementada sobre lista de adyacencia
    con diccionario de diccionarios.
    """ #O diccionario de conjuntos

    def __init__(self):
        """Constructor de la clase grafo."""
        self.vertices = {}

    def agregar_vertice(self, nombre):
        """Recibe un vertice y lo agrega."""
        self.vertices[nombre] = Vertice(nombre)

    def agregar_arista(self, nombre1, nombre2, peso=None):
        """Recibe dos vertices y crea una arista entre ellos,
        del primero al segundo.
        También puede recibir el peso. En caso de que no lo reciba,
        el peso sera None."""
        self.vertices[nombre1].agregar(nombre2, peso)

    def peso_union(self, nombre1, nombre2):
        return self.vertices[nombre1].union(nombre2)

    def adyacentes(self, nombre):
        """Recibe un vertice y devuelve sus adyacentes"""
        return self.vertices[nombre].adyacentes_vertice()

    def eliminar_vertice(self, nombre):
        """Recibe un vertice y lo elimina."""
        if nombre in self.vertices:
            for v in self.vertices:
                self.vertices[v].eliminar(nombre)
            self.vertices.pop(nombre)

    def eliminar_arista(self, nombre1, nombre2):
        """Recibe dos vertices y elimina la arista entre ellos."""
        self.vertices[nombre1].eliminar(nombre2)

    def obtener_vertices(self):
        """Devuelve una lista con todos los vertices del grafo"""
        return list(self.vertices)

    def __str__(self):
        return str(self.vertices)

    def __iter__(self):
        """Crea un iterador de grafo"""
        return _Iter_Grafo_(self.vertices)

class _Iter_Grafo_:
    """
    Clase Iterador del Grafo.
    """
    def __init__(self, vertices):
        """Inicializa un iterador de diccionarios"""
         self.iter = iter(vertices)
    def __next__(self):
        """Itera a la siguiente clave del diccionario, en caso de no existir levanta 'StopIteration'"""
        return next(self.iter)
