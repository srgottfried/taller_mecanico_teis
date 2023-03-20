from models import Factura, Coche


class Cliente:
    def __init__(self,
                 dni=None,
                 nombre=None,
                 alta=None,
                 direccion=None,
                 provincia=None,
                 municipio=None,
                 pago=None):
        self._dni = dni
        self._nombre = nombre
        self._alta = alta
        self._direccion = direccion
        self._provincia = provincia
        self._municipio = municipio
        self._pago = pago
        self._facturas = []
        self._coches = []

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, dni):
        self._dni = dni

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def alta(self):
        return self._alta

    @alta.setter
    def alta(self, alta):
        self._alta = alta

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion

    @property
    def provincia(self):
        return self._provincia

    @provincia.setter
    def provincia(self, provincia):
        self._provincia = provincia

    @property
    def municipio(self):
        return self._municipio

    @municipio.setter
    def municipio(self, municipio):
        self._municipio = municipio

    @property
    def pago(self):
        return self._pago

    @pago.setter
    def pago(self, pago):
        self._pago = pago

    @property
    def facturas(self) -> list[Factura]:
        return self._facturas

    def addFactura(self, factura: Factura):
        self._facturas.append(factura)
        factura.cliente = self
        factura.id_cliente = self.dni

    def addFacturas(self, facturas: list[Factura]):
        for f in facturas:
            self.addFactura(f)

    @property
    def coches(self) -> list[Coche]:
        return self._coches

    def addCoche(self, coche: Coche):
        self._coches.append(coche)
        coche.propietario = self
        coche.propietario_id = self.dni

    def addCoches(self, coches: list[Coche]):
        for c in coches:
            self.addCoche(c)

    def __str__(self):
        return f'Cliente[{self.dni} - {self.nombre}]'

    def __repr__(self):
        return f'Cliente[{self.dni} - {self.nombre}]'
