class Ciudad:
    """
    Clase Ciudad
    """

    def __init__(self):
        """
        Constructor de clase Ciudad.
        """
        self.aeropuertos = {}

    def agregar_aeropuerto(self, aeropuerto, latitud, longitud):
        """
        Recibe un aeropuerto, su latitud y longitud y lo agrega
        a la Ciudad.
        """
        self.aeropuertos[aeropuerto] = [latitud, longitud]

    def info_aeropuerto(self, aeropuerto):
        """
        Recibe un aeropuerto y devuelve su informacion.
        """
        return self.aeropuertos[aeropuerto]

    def ver_aeropuertos(self):
        """
        Devuelve una lista de todos los aeropuertos de la ciudad.
        """
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
