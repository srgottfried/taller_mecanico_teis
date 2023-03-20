from models import Provincia


class Municipio:
    def __init__(self,
                 id: int = None,
                 nombre: str = None):
        self._id = id
        self._nombre = nombre
        self._provincia = None

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
    def provincia(self):
        return self._provincia

    @provincia.setter
    def provincia(self, provincia: Provincia):
        self._provincia = provincia

    def add_provincia(self, provincia: Provincia):
        self._provincia = provincia
        provincia.municipios.append(self)

    def __str__(self):
        return f'{self.id} - {self.nombre} - {self.provincia}'

    def __repr__(self):
        return self.nombre
