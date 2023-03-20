import datetime
from datetime import date

from PyQt6 import QtSql
from PyQt6.QtCore import QDateTime

from models import Cliente
from models.Coche import Coche
from services import ConnectionManager


class CocheQtDao:
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def create(coche: Coche):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                            insert into coches(matricula, dnicli, marca, modelo, motor) 
                            values (:matricula, :dnicli, :marca, :modelo, :motor)
                            ''')
            query.bindValue(':matricula', coche.matricula)
            query.bindValue(':dnicli', coche.propietario.dni)
            query.bindValue(':marca', coche.marca)
            query.bindValue(':modelo', coche.modelo)
            query.bindValue(':motor', coche.motor)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al crear un coche en la base de datos: {e}')
            return False

    @staticmethod
    def read(dni: str = None):
        try:
            coches = []
            query = QtSql.QSqlQuery()
            if not dni:
                query.prepare('''
                                select c.matricula, c.marca, c.modelo, c.motor,
                                cli.dni, cli.nombre, cli.alta, cli.direccion, cli.provincia,
                                cli.municipio, cli.pago, c.fecha_baja
                                from coches c inner join clientes cli on cli.dni = c.dnicli
                                where cli.activo = 1 and c.activo = 1
                ''')
            else:
                query.prepare('''
                                select c.matricula, c.marca, c.modelo, c.motor,
                                cli.dni, cli.nombre, cli.alta, cli.direccion, cli.provincia,
                                cli.municipio, cli.pago, c.fecha_baja
                                from coches c inner join clientes cli on cli.dni = c.dnicli
                                where cli.activo= 1 and c.dnicli = :dni
                                ''')
                query.bindValue(':dni', dni)
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(4)
                    cliente.nombre = query.value(5)
                    cliente.alta = query.value(6)
                    cliente.direccion = query.value(7)
                    cliente.provincia = query.value(8)
                    cliente.municipio = query.value(9)
                    cliente.pago = query.value(10)
                    coche = Coche(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        cliente,
                        fecha_baja=query.value(11)
                    )
                    coches.append(coche)
            return coches
        except Exception as e:
            print(f'Error al leer los coches: {e}')

    @staticmethod
    def update(coche: Coche):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                            update coches
                            set marca = :marca,
                                modelo = :modelo,
                                motor = :motor
                            where matricula = :matricula
                            ''')
            query.bindValue(':marca', coche.marca)
            query.bindValue(':modelo', coche.modelo)
            query.bindValue(':motor', coche.motor)
            query.bindValue(':matricula', coche.matricula)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al actualizar un coche de la base de datos: {e}')
            return False

    @staticmethod
    def change_owner(matricula, new_dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                update coches
                                set dnicli = :new_dni
                                where matricula = :matricula
                                ''')
            query.bindValue(':new_dni', new_dni)
            query.bindValue(':matricula', matricula)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al actualizar el propietario de un coche de la base de datos: {e}')
            return False

    @staticmethod
    def restore_by_matricula(dni, matricula):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update coches set activo = 1, fecha_baja = :fecha_baja where matricula = :matricula')
            query.bindValue(':matricula', matricula)
            query.bindValue(':fecha_baja', '')

            query1 = QtSql.QSqlQuery()
            query1.prepare('update clientes set activo = 1, fecha_baja = :vacio where dni = :dni')
            query1.bindValue(':vacio', '')
            query1.bindValue(':dni', dni)

            if query1.exec():
                if query.exec():
                    return True
            else:
                print("error")
                return False
        except Exception as e:
            print(f'Error al restaurar un coche de la base de datos: {e}')
            return False

    @staticmethod
    def delete_by_client_dni(dni):
        try:
            d = str(datetime.date.today().strftime('%d/%m/%Y'))
            query = QtSql.QSqlQuery()
            query.prepare('update coches set activo = 0, fecha_baja = :fecha_baja where dnicli = :dni')
            query.bindValue(':dni', dni)
            query.bindValue(':fecha_baja', d)
            if query.exec():
                return True
            else:
                print("error")
                return False
        except Exception as e:
            print(f'Error al borrar un coche de la base de datos: {e}')
            return False

    @staticmethod
    def exists(matricula: str):
        query = QtSql.QSqlQuery()
        query.prepare('''
                        select count(*) from coches where matricula = :matricula
                    ''')
        query.bindValue(':matricula', matricula)
        if query.exec():
            query.next()
            return query.value(0) > 0

    @staticmethod
    def read_bajas():
        try:
            coches = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select c.matricula, c.marca, c.modelo, c.motor, 
                                cli.dni, cli.nombre, cli.alta, cli.direccion, cli.provincia,
                                cli.municipio, cli.pago, c.fecha_baja
                                from coches c inner join clientes cli on cli.dni = c.dnicli
                                where c.activo = 0
            ''')
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(4)
                    cliente.nombre = query.value(5)
                    cliente.alta = query.value(6)
                    cliente.direccion = query.value(7)
                    cliente.provincia = query.value(8)
                    cliente.municipio = query.value(9)
                    cliente.pago = query.value(10)
                    coche = Coche(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        cliente,
                        fecha_baja=query.value(11)
                    )
                    coches.append(coche)
            return coches
        except Exception as e:
            print(f'Error al leer los coches: {e}')

    @staticmethod
    def read_altas_all():
        try:
            coches = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select c.matricula, c.marca, c.modelo, c.motor, 
                                    cli.dni, cli.nombre, cli.alta, cli.direccion, cli.provincia,
                                    cli.municipio, cli.pago, c.fecha_baja
                                    from coches c inner join clientes cli on cli.dni = c.dnicli
                                    where c.activo = 1
                ''')
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(4)
                    cliente.nombre = query.value(5)
                    cliente.alta = query.value(6)
                    cliente.direccion = query.value(7)
                    cliente.provincia = query.value(8)
                    cliente.municipio = query.value(9)
                    cliente.pago = query.value(10)
                    coche = Coche(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        cliente,
                        fecha_baja=query.value(11)
                    )
                    coches.append(coche)
            return coches
        except Exception as e:
            print(f'Error al leer los coches: {e}')

    @staticmethod
    def read_altas(dni):
        try:
            coches = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select c.matricula, c.marca, c.modelo, c.motor, 
                                    cli.dni, cli.nombre, cli.alta, cli.direccion, cli.provincia,
                                    cli.municipio, cli.pago, c.fecha_baja
                                    from coches c inner join clientes cli on cli.dni = c.dnicli
                                    where c.activo = 1 and cli.dni = :dni
                ''')
            query.bindValue(":dni", dni)
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(4)
                    cliente.nombre = query.value(5)
                    cliente.alta = query.value(6)
                    cliente.direccion = query.value(7)
                    cliente.provincia = query.value(8)
                    cliente.municipio = query.value(9)
                    cliente.pago = query.value(10)
                    coche = Coche(
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        cliente,
                        query.value(11)
                    )
                    coches.append(coche)
            return coches
        except Exception as e:
            print(f'Error al leer los coches: {e}')
