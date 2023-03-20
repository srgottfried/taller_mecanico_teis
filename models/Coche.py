from models import Cliente


class Coche:
    def __init__(self,
                 matricula=None,
                 marca=None,
                 modelo=None,
                 motor=None,
                 propietario: Cliente = None,
                 propietario_id =0,
                 fecha_baja=None,
                 activo = True):

        self._matricula = matricula
        self._marca = marca
        self._modelo = modelo
        self._motor = motor
        self._fecha_baja = fecha_baja
        self._propietario = propietario
        self._propietario_id = propietario_id
        self._activo = activo

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, matricula):
        self._matricula = matricula

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, activo: bool):
        self._activo = activo

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, marca):
        self._marca = marca

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, modelo):
        self._modelo = modelo

    @property
    def motor(self):
        return self._motor

    @motor.setter
    def motor(self, motor):
        self._motor = motor

    @property
    def fecha_baja(self):
        return self._fecha_baja

    @fecha_baja.setter
    def fecha_baja(self, fecha_baja):
        self._fecha_baja = fecha_baja

    @property
    def propietario(self):
        return self._propietario

    @propietario.setter
    def propietario(self, propietaro: Cliente):
        self._propietario = propietaro

    @property
    def propietario_id(self):
        return self._propietario_id

    @propietario_id.setter
    def propietario_id(self, propietario_id):
        self._propietario_id = propietario_id

    def __str__(self):
        return str(f' Coche[{self.matricula} - {self.marca} - {self.modelo} - {self.motor} - {self.propietario_id} - {self.activo}]')

    def __repr__(self):
        return str(f'Coche[{self.matricula}, {self.propietario_id}, {self.activo}]')
