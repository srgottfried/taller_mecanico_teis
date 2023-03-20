from PyQt6 import QtSql
from PyQt6.QtSql import QSqlQuery

from models import Servicio
from services import ConnectionManager


class ServicioQtDao:
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def read():
        try:
            servicios = []
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, concepto, "precio-unidad", stock from servicios')
            if query.exec():
                while query.next():
                    servicio = Servicio()
                    servicio.codigo = query.value(0)
                    servicio.concepto = query.value(1)
                    servicio.precio_unidad = query.value(2)
                    servicio.stock = query.value(3)
                    servicios.append(servicio)

            return servicios

        except Exception as e:
            print(f'Error al leer los servicios de la base de datos: {e}')

    @staticmethod
    def read_by_id(id):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, concepto, "precio-unidad", stock from servicios where codigo = :id')
            query.bindValue(':id', id)
            serv = None
            if query.exec():
                serv = Servicio()
                serv.codigo = query.value(0)
                serv.concepto = query.value(1)
                serv.precio_unidad = query.value(2)
                serv.stock = query.value(3)
            return serv

        except Exception as e:
            print(f'Error al leer los servicios de la base de datos: {e}')

    @staticmethod
    def create(servicio: Servicio):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into servicios (concepto, "precio-unidad", stock) values (:concepto, :precio, :stock)')
            query.bindValue(':concepto', servicio.concepto)
            query.bindValue(':precio', servicio.precio_unidad)
            query.bindValue(':stock', servicio.stock)

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al insertar un nuevo servicio en la base de datos: {e}')

    @staticmethod
    def delete(codigo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from servicios where codigo = :codigo')
            query.bindValue(':codigo', str(codigo))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al borrar un servicio de la base de datos: {e}')

    @staticmethod
    def update(servicio: Servicio):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                               update servicios
                               set concepto = :concepto,
                                   "precio-unidad" = :precio,
                                   stock = :stock
                               where codigo = :codigo
                               ''')
            query.bindValue(':concepto', servicio.concepto)
            query.bindValue(':precio', servicio.precio_unidad)
            query.bindValue(':codigo', servicio.codigo)
            query.bindValue(':stock', servicio.stock)

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al actualizar un servicio de la base de datos: {e}')
            return False
