from PyQt6 import QtSql

from models import Factura, Servicio
from services import ConnectionManager


class FacturaQtDao:
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def read_by_id():
        try:
            factura = Factura()
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, cliente_id, linea_factura_id, fecha, matricula from facturas')
            if query.exec():
                while query.next():
                    factura.codigo = query.value(0)
                    factura.cliente = query.value(1)
                    factura.servicios = query.value(2)
                    factura.fecha = query.value(3)
                    factura.coche = query.value(4)

            return factura

        except Exception as e:
            print(f'Error al leer la factura por id de la base de datos: {e}')

    @staticmethod
    def read_by_cliente_id(cliente_id):
        try:
            factura = Factura()
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, cliente_id, linea_factura_id, fecha, matricula from facturas where cliente_id = :cliente_id')
            query.bindValue(':cliente_id', cliente_id)
            if query.exec():
                while query.next():
                    factura.codigo = query.value(0)
                    factura.cliente = query.value(1)
                    factura.servicios = query.value(2)
                    factura.fecha = query.value(3)
                    factura.coche = query.value(4)

            return factura

        except Exception as e:
            print(f'Error al leer la factura por id de la base de datos: {e}')

    @staticmethod
    def read():
        try:
            facturas = []

            query = QtSql.QSqlQuery()
            query.prepare('select codigo, cliente_id from facturas')
            if query.exec():
                while query.next():
                    factura = Factura()

                    factura.codigo = int(query.value(0))
                    factura.cliente = str(query.value(1))

                    query2 = QtSql.QSqlQuery()
                    query2.prepare('select matricula from coches where dnicli = :dnicli')
                    query2.bindValue(':dnicli', query.value(1))
                    if query2.exec():
                        while query2.next():
                            factura.matricula = query2.value(0)

                    facturas.append(factura)

            return facturas

        except Exception as e:
            print(f'Error al leer las facturas de la base de datos: {e}')

    @staticmethod
    def create(factura: Factura):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'INSERT INTO facturas(codigo, cliente_id, linea_factura_id, fecha) VALUES (:codigo, :cliente_id, :linea_factura_id, :fecha)')
            query.bindValue(':codigo', factura.codigo_factura)
            query.bindValue(':cliente_id', factura.cliente.dni)
            query.bindValue(':linea_factura_id', None)  # TODO
            query.bindValue(':fecha', factura.fecha)

        except Exception as e:
            print(f'Error al insertar una nueva factura en la base de datos: {e}')

    @staticmethod
    def delete_by_codigo(codigo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('DELETE FROM facturas WHERE linea_factura_id = :codigo')
            query.bindValue(':codigo', codigo)
            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print(f'Error al borrar una factura de la base de datos: {e}')
            return False

    @staticmethod
    def update(factura: Factura):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                        update facturas
                                        set cliente_id = :cliente_id,
                                            linea_factura_id = :linea_factura_id,
                                            fecha = :fecha
                                        where codigo = :codigo
                                        ''')
            query.bindValue(':cliente_id', factura.cliente.dni)
            query.bindValue(':linea_factura_id', None)  # TODO
            query.bindValue(':fecha', factura.fecha)
            query.bindValue(':codigo', factura.codigo_factura)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al actualizar una factura de la base de datos: {e}')
            return False

    @staticmethod
    def exists(id):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('SELECT count(*) FROM facturas WHERE codigo = :codigo')
            query.bindValue(':codigo', id)
            if query.exec():
                query.next()
                return query.value(0) > 0

        except Exception as e:
            print(f'Error al verificar la existencia de la factura en la base de datos: {e}')
