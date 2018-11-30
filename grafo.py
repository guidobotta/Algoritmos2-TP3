from random import choice

class Grafo:
    """
    Clase Grafo implementada sobre lista de adyacencia
    con diccionario de diccionarios.
    """

    def __init__(self):
        """
        Constructor de la clase grafo.
        """
        self.vertices = {}

    def agregar_vertice(self, vertice):
        """
        Recibe un vertice y lo agrega.
        """
        if not vertice in self.vertices:
            self.vertices[vertice] = {}
        else:
            raise Exception()

    def agregar_arista(self, vertice_1, vertice_2, peso=None):
        """
        Recibe dos vertices y crea una arista entre ellos,
        del primero al segundo.
        También puede recibir el peso. En caso de que no lo reciba,
        el peso sera None.
        En caso de existir la arista, la nueva arista pisa a la anterior.
        """
        if (vertice_1 in self.vertices) and (vertice_2 in self.vertices):
            self.vertices[vertice_1][vertice_2] = peso
        else:
            raise Exception()

    def peso_arista(self, vertice_1, vertice_2):
        """
        Recibe dos vertices y devuelve el peso de la arista del vertice 1
        al vertice 2.
        """
        if (vertice_1 in self.vertices) and (vertice_2 in self.vertices)\
        and (vertice_2 in self.vertices[vertice_1]):
            return self.vertices[vertice_1][vertice_2]
        raise Exception()

    def adyacentes(self, vertice):
        """
        Recibe un vertice y devuelve una lista de sus adyacentes.
        """
        if vertice in self.vertices:
            return list(self.vertices[vertice])
        else:
            raise Exception()

    def aristas(self):
        """
        Devuelve una lista de las aristas (diccionario).
        """
        return list(self.vertices.values())

    def eliminar_vertice(self, vertice):
        """
        Recibe un vertice y lo elimina.
        """
        if vertice in self.vertices:
            for v in self.vertices:
                try:
                    self.vertices[v].pop(vertice)
                except:
                    continue
        else:
            raise Exception()

    def eliminar_arista(self, vertice_1, vertice_2):
        """
        Recibe dos vertices y elimina la arista entre ellos.
        """
        if (vertice_1 in self.vertices) and (vertice_2 in self.vertices)\
        and (vertice_2 in self.vertices[vertice_1]):
            self.vertices[vectice_1].pop(vertice_2)
        else:
            raise Exception()

    def obtener_vertices(self):
        """
        Devuelve una lista con todos los vertices del grafo.
        """
        return list(self.vertices)

    def obtener_vertice_aleatorio(self):
        """
        Devuelve un vertice cualquier del grafo.
        """
        return choice(self.obtener_vertices())

    def __len__(self):
        """
        Devuelve la cantidad de vertices que contiene el grafo.
        """
        return len(self.vertices)

    def __iter__(self):
        """
        Crea un iterador de grafo.
        """
        return _Iter_Grafo_(self.vertices)

class _Iter_Grafo_:
    """
    Clase Iterador del Grafo.
    """

    def __init__(self, vertices):
        """
        Inicializa un iterador de diccionarios.
        """
        self.iter = iter(vertices)

    def __next__(self):
        """
        Itera a la siguiente clave del diccionario, en caso de no
        existir, levanta 'StopIteration'.
        """
        return next(self.iter)
