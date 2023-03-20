import datetime

from PyQt6 import QtSql
from models import Cliente, Factura
from services import ConnectionManager

'''
Objeto de acceso a datos de Cliente en el contexto de un flujo de trabajo de QApplication.
'''


class ClienteQtDao:
    def __init__(self):
        # Establecemos conexión sólo si no existe una ya establecida en el flujo de la app.
        ConnectionManager.connect()

    @staticmethod
    def create(cliente: Cliente):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                            insert into clientes(dni, nombre, alta, direccion, provincia, municipio, pago) 
                            values (:dni, :nombre, :alta, :direccion, :provincia, :municipio, :pago)
                            ''')
            query.bindValue(':dni', cliente.dni)
            query.bindValue(':nombre', cliente.nombre)
            query.bindValue(':alta', cliente.alta)
            query.bindValue(':direccion', cliente.direccion)
            query.bindValue(':provincia', cliente.provincia)
            query.bindValue(':municipio', cliente.municipio)
            query.bindValue(':pago', cliente.pago)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al crear un cliente en la base de datos: {e}')
            return False

    @staticmethod
    def read(dni=None):
        try:
            clientes = []
            query = QtSql.QSqlQuery()
            if not dni:
                query.prepare('''
                            select dni, nombre, alta, direccion, provincia, municipio, pago 
                            from clientes
                            where activo = 1
                                ''')
            else:
                query.prepare('''
                            select dni, nombre, alta, direccion, provincia, municipio, pago 
                            from clientes
                            where activo = 1 and dni = :dni
                                ''')
                query.bindValue(':dni', dni)
            if query.exec():
                while query.next():
                    clientes.append(Cliente(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        query.value(4),
                        query.value(5),
                        query.value(6)
                    ))
            return clientes
        except Exception as e:
            print(f'Error al leer los clientes: {e}')

    @staticmethod
    def read_by_dni(dni):
        try:
            cliente = Cliente()
            query = QtSql.QSqlQuery()
            query.prepare('''
                            select dni, nombre, alta, direccion, provincia, municipio, pago 
                            from clientes
                            where activo = 1 and dni = :dni
                                ''')
            query.bindValue(':dni', dni)
            if query.exec():
                while query.next():
                    cliente = Cliente(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        query.value(4),
                        query.value(5),
                        query.value(6)
                    )

            query.prepare('''
                            select codigo, cliente_id, fecha, matricula
                            from facturas
                            where cliente_id = :dni
                                            ''')
            query.bindValue(":dni", dni)
            facturas = []
            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    facturas.append(factura)

            cliente.addFacturas(facturas)

            return cliente

        except Exception as e:
            print(f'Error al leer el cliente: {e}')

    @staticmethod
    def readAll():
        try:
            clientes = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                            select dni, nombre, alta, direccion, provincia, municipio, pago 
                            from clientes
                                ''')
            if query.exec():
                while query.next():
                    clientes.append(Cliente(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        query.value(4),
                        query.value(5),
                        query.value(6)
                    ))
            return clientes
        except Exception as e:
            print(f'Error al leer los clientes: {e}')

    @staticmethod
    def update(cliente: Cliente):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                            update clientes
                            set nombre = :nombre,
                                alta = :alta,
                                direccion = :direccion,
                                provincia = :provincia,
                                municipio = :municipio,
                                pago = :pago
                            where dni = :dni
                            ''')
            query.bindValue(':dni', cliente.dni)
            query.bindValue(':nombre', cliente.nombre)
            query.bindValue(':alta', cliente.alta)
            query.bindValue(':direccion', cliente.direccion)
            query.bindValue(':provincia', cliente.provincia)
            query.bindValue(':municipio', cliente.municipio)
            query.bindValue(':pago', cliente.pago)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al actualizar un cliente de la base de datos: {e}')
            return False

    @staticmethod
    def delete(cliente: Cliente):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from clientes where dni = :dni')
            query.bindValue(':dni', cliente.dni)
        except Exception as e:
            print(f'Error al borrar un clinete de la base de datos: {e}')

    @staticmethod
    def delete_by_dni(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set activo = 0, fecha_baja = :hoy  where dni = :dni')
            query.bindValue(':hoy', str(datetime.date.today().strftime('%d/%m/%Y')))
            query.bindValue(':dni', str(dni))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al borrar un clinete de la base de datos: {e}')
            return False

    @staticmethod
    def exists(cliente: Cliente):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select count(*) from clientes where dni = :dni')
            query.bindValue(':dni', cliente.dni)
            if query.exec():
                query.next()
                return query.value(0) > 0
        except Exception as e:
            print(f'Error al confirmar existencia de cliente en base de datos: {e}')

    @staticmethod
    def exists_dni(dni):
        query = QtSql.QSqlQuery()
        query.prepare('select count(*) from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec():
            query.next()
            return query.value(0) > 0
