from PyQt6 import QtSql

from models import LineaFactura, Factura, Servicio
from services import ConnectionManager


class LineaFacturaQtDao:
    ConnectionManager.connect()

    @staticmethod
    def read():
        try:
            lineas = []
            linea = LineaFactura()
            query = QtSql.QSqlQuery()
            query.prepare('select id, id_factura, id_servicio, precio, unidades form ventas')
            if query.exec():
                while query.next():
                    linea.id = query.value(0)
                    linea.factura = query.value(1)
                    linea.servicio = query.value(2)
                    linea.precio = query.value(3)
                    linea.unidades = query.value(4)

                    lineas.append(linea)

            return lineas

        except Exception as e:
            print(f'Error al leer las lineas de factura de la base de datos: {e}')

    @staticmethod
    def read_by_id(id_factura):
        try:
            lineas_factura = []

            query = QtSql.QSqlQuery()
            query.prepare('''
                            select id, id_factura, id_servicio, precio, unidades
                            from lineas_factura
                            where id_factura = :id_factura
                                ''')
            query.bindValue(':id_factura', id_factura)
            if query.exec():
                while query.next():
                    linea = LineaFactura()
                    linea.id = query.value(0)
                    linea.query.value(2),
                    query.value(3),
                    query.value(4)

        except Exception as e:
            print(f'Error al leer el cliente: {e}')

    @staticmethod
    def create(linea_factura: LineaFactura):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                INSERT INTO lineas_factura (id_factura, id_servicio, precio, unidades) 
                                VALUES (':id_factura', ':id_servicio', ':precio', ':unidades') 
                                            ''')
            query.bindValue(':id_factura', linea_factura.factura.codigo_factura or None)
            query.bindValue(':id_servicio', linea_factura.servicio.codigo or None)
            query.bindValue(':precio', linea_factura.precio)
            query.bindValue(':unidades', linea_factura.unidades)

            return query.exec()

        except Exception as e:
            print(f'Error al crear linea de factura: {e}')

    @staticmethod
    def delete_by_id(id):
        pass

    @staticmethod
    def update(linea_factura: LineaFactura):
        pass

    @staticmethod
    def exists(id):
        pass