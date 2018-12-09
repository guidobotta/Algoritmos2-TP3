class Heap:
    """Representa a un Heap de máximos (o cola de prioridad), 
    con operaciones de encolar, desencolar, ver_cantidad, ver_max 
    y esta_vacia."""

    def __init__(self, cmp):
        """
        Constructor de la clase Heap. Recibe una función de comparación
        que devuelve un entero:
        cmp(a,b) < 0 si a < b
        cmp(a,b) = 0 si a = b
        cmp(a,b) > 0 si a > b
        """
        self.heap = []
        self.cmp = cmp

    def ver_cantidad(self):
        """Devuelve la cantidad de elementos."""
        return len(self.heap)

    def esta_vacia(self):
        """Devuelve True si el Heap está vacío o False si no lo está."""
        return len(self.heap) == 0

    def swap(self, pos, padre):
        """Swapea al actual con su padre."""
        self.heap[padre], self.heap[pos] = self.heap[pos], self.heap[padre]

    def up_heap(self, pos):
        """Aplica up_heap al actual"""
        padre = (pos-1)//2
        if (padre < 0) or (self.cmp(self.heap[pos], self.heap[padre]) < 0): 
            return
        self.swap(padre, pos)
        self.up_heap(padre)

    def down_heap(self, pos):
        """Aplica down_heap al actual"""
        hijo_izq = (2*pos) + 1
        hijo_der = (2*pos) + 2

        if (hijo_der < len(self.heap)) and (self.cmp(self.heap[pos], self.heap[hijo_der]) < 0):

            if self.cmp(self.heap[hijo_izq], self.heap[hijo_der]) > 0:
                self.swap(pos, hijo_izq)
                self.down_heap(hijo_izq)

            else:
                self.swap(pos, hijo_der)
                self.down_heap(hijo_der)

        elif (hijo_izq < len(self.heap)) and (self.cmp(self.heap[pos], self.heap[hijo_izq]) < 0):
            self.swap(pos, hijo_izq)
            self.down_heap(hijo_izq)

    def encolar(self, elemento):
        """Recibe un elemento y lo encola"""
        self.heap.append(elemento)
        self.up_heap(len(self.heap)-1)

    def desencolar(self):
        """Desencola el máximo elemento y lo devuelve."""
        if self.esta_vacia():
            return None
        self.swap(0, len(self.heap)-1)
        valor = self.heap.pop()
        self.down_heap(0)
        return valor

    def ver_max(self):
        """Devuelve el máximo elemento del Heap.
        En caso de estar vacío devuelve None."""
        if self.esta_vacia():
            return None
        return self.heap[0]

    def __str__(self):
        return str(self.heap)