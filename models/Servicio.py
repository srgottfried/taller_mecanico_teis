class Servicio:
    def __init__(self,
                 codigo=None,
                 concepto=None,
                 precio_unidad=None,
                 stock=0):

        self._codigo = codigo
        self._concepto = concepto
        self._precio_unidad = precio_unidad
        self._stock = stock

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @property
    def concepto(self):
        return self._concepto

    @concepto.setter
    def concepto(self, concepto):
        self._concepto = concepto

    @property
    def precio_unidad(self):
        return self._precio_unidad

    @precio_unidad.setter
    def precio_unidad(self, precio_unidad):
        self._precio_unidad = precio_unidad

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    def __str__(self):
        return f'Servicio[{self._codigo}, {self._concepto}, {self._precio_unidad}, {self._stock}]'

    def __repr__(self):
        return f'Servicio[{self._codigo}, {self._concepto}, {self._precio_unidad}, {self._stock}]'
