class Ciudad:
    def __init__(self):
        self.aeropuertos = {}

    def agregar_aeropuerto(self, aeropuerto, latitud, longitud):
        self.aeropuertos[aeropuerto] = [latitud, longitud]

    def info_aeropuerto(self, aeropuerto):
        return self.aeropuertos[aeropuerto]

    def ver_aeropuertos(self):
        return list(self.aeropuertos.keys())

    def __iter__(self):
        """Crea un iterador de ciudad"""
        return _Iter_Ciudad_(self.aeropuertos)

class _Iter_Ciudad_:
    """
    Clase Iterador de Ciudad.
    """
    def __init__(self, aeropuertos):
        """Inicializa un iterador de diccionarios"""
        self.iter = iter(aeropuertos)
    def __next__(self):
        """Itera a la siguiente clave del diccionario, en caso de no existir levanta 'StopIteration'"""
        return next(self.iter)
