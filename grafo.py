class Vertice:

    def __init__(self, nombre):
        """Constructor de la clase grafo."""
        self.adyacentes = {}

    def agregar(self, nombre, peso):
        self.adyacentes[nombre] = peso

    def eliminar(self, nombre):
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
        self.adyacentes = {}

    def agregar_vertice(self, nombre):
        """Recibe un vertice y lo agrega."""
        self.adyacentes[nombre] = Vertice(nombre)

    def agregar_arista(self, nombre1, nombre2, peso=None):
        """Recibe dos vertices y crea una arista entre ellos,
        del primero al segundo.
        También puede recibir el peso. En caso de que no lo reciba,
        el peso sera None."""
        self.adyacentes[nombre1].agregar(nombre2, peso)

    def eliminar_vertice(self, nombre):
        """Recibe un vertice y lo elimina."""
        if nombre in self.adyacentes:
            for v in self.adyacentes:
                self.adyacentes[v].eliminar(nombre)
            self.adyacentes.pop(nombre)

    def eliminar_arista(self, nombre1, nombre2):
        """Recibe dos vertices y elimina la arista entre ellos."""
        self.adyacentes[nombre1].eliminar(nombre2)

    def __str__(self):
        return str(self.adyacentes)