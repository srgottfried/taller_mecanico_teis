from models import Servicio, Factura


class LineaFactura:

    def __init__(self,
                 servicio: Servicio,
                 id_factura=0,
                 unidades=1.0):
        self._id = None
        self._servicio = servicio
        self._id_factura = id_factura
        self._unidades = float(unidades)
        self._precio = float(servicio.precio_unidad.replace(',', '.')) * int(unidades)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @servicio.setter
    def servicio(self, servicio: Servicio):
        self._servicio = servicio

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, precio):
        self._precio = precio

    @property
    def id_factura(self):
        return self._id_factura

    @id_factura.setter
    def id_factura(self, id_factura):
        self._id_factura = id_factura

    @property
    def unidades(self):
        return self._unidades

    @unidades.setter
    def unidades(self, unidades: float):
        self._unidades = float(unidades)

    def calcular_subtotal(self):
        return self.precio * self.unidades

    def __str__(self):
        return f'LineaFactura[{self.servicio.concepto}, {self.unidades}, {self.precio}, {self._id_factura}]'

    def __repr__(self):
        return f'LineaFactura[{self.servicio.concepto}, {self.unidades}, {self.precio}, {self._id_factura}]'
