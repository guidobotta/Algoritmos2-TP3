class Heap:

    def __init__(self, cmp):
        self.heap = []
        self.cantidad = 0
        self.cmp = cmp

    def ver_cantidad(self):
        return self.cantidad

    def swap(self, pos, padre):
        aux = self.heap[padre]
        self.heap[padre] = self.heap[pos]
        self.heap[pos] = aux

    def up_heap(self, pos):
        padre = (pos-1)//2
        if padre < 0 or self.cmp(self.heap[pos], self.heap[padre]) < 0: return
        self.swap(padre, pos)
        self.up_heap(padre)

    def down_heap(self, pos):
        hijo_izq = (2*pos) + 1;
        hijo_der = (2*pos) + 2;

        if hijo_der < self.cantidad and self.cmp(self.heap[pos], self.heap[hijo_der]) < 0:
            if self.cmp(self.heap[hijo_izq], self.heap[hijo_der]) > 0:
                self.swap(pos, hijo_izq)
                self.down_heap(hijo_izq)
            else:
                self.swap(pos, hijo_der)
                self.down_heap(hijo_der)
        elif hijo_izq < self.cantidad and self.cmp(self.heap[pos], self.heap[hijo_izq]) < 0:
            self.swap(pos, hijo_izq)
            self.down_heap(hijo_izq)

    def encolar(self, elemento):
        self.heap.append(elemento)
        self.up_heap(self.cantidad)
        self.cantidad += 1


    def desencolar(self):
        self.cantidad -=1
        valor = self.heap.pop(0)
        self.down_heap(0)
        return valor


    def __str__(self):

        return str(self.heap)

class Cola:

    def __init__(self):
        self.cola = []
        self.cantidad = 0
    def ver_cantidad(self):
        return self.cantidad
    def encolar(self, elemento):
        self.cola.append(elemento)
        self.cantidad +=1
    def desencolar(self):
        valor = self.cola.pop(0)
        self.cantidad -= 1
        return valor
    def __str__(self):
        return str(self.cola)

class Pila:

    def __init__(self):
        self.pila = []
        self.cantidad = 0
    def ver_cantidad(self):
        return self.cantidad
    def apilar(self, elemento):
        self.pila.append(elemento)
        self.cantidad +=1
    def desapilar(self):
        self.cantidad -= 1
        valor = self.pila.pop(self.cantidad)

        return valor
    def __str__(self):
        return str(self.pila)



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


    def agregar_arista(self, nombre1, nombre2, peso):
        #Se puede hacer que recibe una tupla de dos vertices
        """"""
        self.adyacentes[nombre1].agregar(nombre2, peso)

    def eliminar_vertice(self, nombre):
        """Recibe un vertice y lo elimina."""
        if nombre in self.adyacentes:
            for v in self.adyacentes:
                self.adyacentes[v].eliminar(nombre)
            self.adyacentes.pop(nombre)

    def eliminar_arista(self, nombre1, nombre2):
        """"""
        self.adyacentes[nombre1].eliminar(nombre2)
    def __str__(self):

        return str(self.adyacentes)


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


def comparacion(x, y):
    if x > y: return 1
    if x < y: return -1
    return 0

def main():

    grafo = Grafo()
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")
    grafo.agregar_vertice("F")
    grafo.agregar_arista("A","B", 1)
    grafo.agregar_arista("B","A", 2)
    grafo.agregar_arista("A","C", 3)
    grafo.agregar_arista("C","E", 1)
    grafo.agregar_arista("B","F", 2)
    grafo.agregar_arista("F","D", 3)
    grafo.agregar_arista("D","B", 1)
    grafo.agregar_arista("D","A", 2)
    grafo.agregar_arista("F","B", 3)
    grafo.agregar_arista("E","A", 2)
    grafo.agregar_arista("E","B", 3)

    #print(grafo)
    for v in grafo.adyacentes:
        print(v + ":" + str(grafo.adyacentes[v]))



    print("/" * 50)
    #grafo.eliminar_vertice("B")
    grafo.eliminar_arista("A", "B")

    for v in grafo.adyacentes:
        print(v + ":" + str(grafo.adyacentes[v]))
    #print(grafo.adyacentes["A"])

main()
