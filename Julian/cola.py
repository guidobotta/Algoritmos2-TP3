class Cola:
    """Representa a una cola, con operaciones de encolar,
	desencolar, ver_cantidad, esta_vacia y ver_primero."""

    def __init__(self):
        """Constructor de la clase Cola"""
        self.cola = []

    def ver_cantidad(self):
        """Devuelve la cantidad de elementos que tiene la cola."""
        return len(self.cola)

    def esta_vacia(self):
        """Devuelve True si la cola está vacía, o False si no lo está."""
        return len(self.cola) == 0

    def ver_primero(self):
        """Devuelve el primer elemento de la cola.
        En caso de que este vacía, devuelve None"""
        if self.esta_vacia():
            return None
        return self.cola[0]

    def encolar(self, elemento):
        """Recibe un elemento y lo encola."""
        self.cola.append(elemento)

    def desencolar(self):
        """Desencola el primer elemento y lo devuelve.
        En caso de estar vacía, devuelve None."""
        if self.esta_vacia():
            return None
        return self.cola.pop(0)

    def __str__(self):
        return str(self.cola)