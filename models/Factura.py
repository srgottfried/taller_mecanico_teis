from models import LineaFactura, Cliente


class Factura:
    def __init__(self):
        self._codigo = None
        self._cliente = None
        self._id_cliente = 0
        self._matricula = None
        self._emitida = 0
        self._fecha = '0'
        self._lineas_de_factura = []
        self._descuento = 0

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, descuento):
        self._descuento = descuento

    @property
    def codigo_factura(self):
        return self._codigo

    @codigo_factura.setter
    def codigo_factura(self, codigo_factura):
        self._codigo = codigo_factura

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, id_cliente):
        self._id_cliente = id_cliente

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, cliente: Cliente):
        self._cliente = cliente

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, matricula):
        self._matricula = matricula

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, fecha):
        self._fecha = fecha

    @property
    def emitida(self):
        return self._emitida

    @emitida.setter
    def emitida(self, emitida):
        self._emitida = emitida

    def emitir_factura(self):
        self._emitida = True

    @property
    def lineas_de_factura(self) -> list[LineaFactura]:
        return self._lineas_de_factura

    def add_linea_factura(self, linea_factura: LineaFactura):
        self._lineas_de_factura.append(linea_factura)
        linea_factura.id_factura = self.codigo_factura

    def add_lineas_de_factura(self, lista_lineas_de_factura: list[LineaFactura]):
        for linea in lista_lineas_de_factura:
            self.add_linea_factura(linea)

    def __str__(self):
        return f'Factura[{self.codigo_factura}, {self.id_cliente}]'

    def __repr__(self):
        return f'Factura[{self.codigo_factura}, {self.id_cliente}]'

    def __eq__(self, other):
        return self.codigo_factura == other.codigo_factura
