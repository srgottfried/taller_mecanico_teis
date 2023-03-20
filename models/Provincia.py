class Provincia:
    def __init__(self,
                 id: int = None,
                 nombre: str = None):
        self._id = id
        self._nombre = nombre
        self._municipios = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def municipios(self):
        return self._municipios

    @municipios.setter
    def municipios(self, municipios: list):
        self._municipios = municipios

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return self.nombre
