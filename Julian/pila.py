class Pila:
    """Representa una pila con operaciones de apilar, desapilar,
    esta_vacia, ver_tope y ver_cantidad."""

    def __init__(self):
        """Constructor de la clase Pila."""
        self.pila = []

    def ver_cantidad(self):
        """Devuelve la cantidad de elementos que hay en la pila."""
        return len(self.pila)

    def esta_vacia(self):
        """Devuelve True si la pila está vacía, o False si no lo está."""
        return len(self.pila) == 0

    def ver_tope(self):
        """Devuelve el tope de la pila.
        En caso de que esté vacía, devuelve None."""
        if self.esta_vacia():
            return None
        return self.pila[len(self.pila)-1]

    def apilar(self, elemento):
        """Recibe un elemento y lo apila."""
        self.pila.append(elemento)

    def desapilar(self):
        """Desapila el último elemento y lo devuelve.
        En caso de estar vacía, devuelve None."""
        if self.esta_vacia():
            return None
        return self.pila.pop()

    def __str__(self):
        return str(self.pila)