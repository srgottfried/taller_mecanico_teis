from PyQt6 import QtSql

from models import Cliente
from repositories import CocheRepository, FacturaRepository
from services import ConnectionManager


class ClienteRepository:
    """
    Clase repositorio encargada de la persistencia de datos asociados a la clae Cliente.
    """
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def getAll() -> list[Cliente]:
        """

        Obtiene una lista con todos los clientes de la base de datos.

        :return: lista de clientes
        """
        try:
            clientes = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select dni, nombre, alta, direccion, provincia, municipio, pago, activo 
                                from clientes
                                where activo = 1
                ''')
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(0)
                    cliente.nombre = query.value(1)
                    cliente.alta = query.value(2)
                    cliente.direccion = query.value(3)
                    cliente.provincia = query.value(4)
                    cliente.municipio = query.value(5)
                    cliente.pago = query.value(6)

                    cliente.addCoches(CocheRepository.getByDni(cliente.dni))
                    cliente.addFacturas(FacturaRepository.getByClienteId(cliente.dni))

                    clientes.append(cliente)
            return clientes

        except Exception as e:
            print(f'Error al leer los clientes de la base de datos: {e}')

    @staticmethod
    def getById(id) -> Cliente:
        """

        Obtiene cliente por id.

        :param id: del cliente
        :return: cliente
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select dni, nombre, alta, direccion, provincia, municipio, pago, activo 
                                    from clientes
                                    where activo = 1 and dni = :id
                    ''')
            query.bindValue(':id', id)
            cliente = None
            if query.exec():
                while query.next():
                    cliente = Cliente()
                    cliente.dni = query.value(0)
                    cliente.nombre = query.value(1)
                    cliente.alta = query.value(2)
                    cliente.direccion = query.value(3)
                    cliente.provincia = query.value(4)
                    cliente.municipio = query.value(5)
                    cliente.pago = query.value(6)

                    cliente.addCoches(CocheRepository.getByDni(cliente.dni))
                    cliente.addFacturas(FacturaRepository.getByClienteId(cliente.dni))

            return cliente

        except Exception as e:
            print(f'Error al leer los clientes de la base de datos: {e}')

    @staticmethod
    def save(cliente: Cliente) -> bool:
        """

        Guarda objeto cliente y persiste en cascada todos los objetos asociados.

        :param cliente: a guardar
        :return: si éxito
        """
        if not ClienteRepository.exists(cliente):
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                        INSERT INTO clientes (dni, nombre, alta, direccion, provincia, municipio, pago)
                                        VALUES (:dni, :nombre, :alta, :direccion, :provincia, :municipio, :pago)
                        ''')

                query.bindValue(':dni', cliente.dni)
                query.bindValue(':nombre', cliente.nombre)
                query.bindValue(':alta', cliente.alta)
                query.bindValue(':direccion', cliente.direccion)
                query.bindValue(':provincia', cliente.provincia)
                query.bindValue(':municipio', cliente.municipio)
                query.bindValue(':pago', cliente.pago)

                if cliente.coches is not []:
                    for coche in cliente.coches:
                        CocheRepository.save(coche)

                if cliente.facturas is not []:
                    for factura in cliente.facturas:
                        FacturaRepository.save(factura)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar un coche en la base de datos: {e}')

        else:
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                    UPDATE clientes 
                                    set nombre = :nombre,
                                    alta = :alta,
                                    direccion = :direccion,
                                    provincia = :provincia,
                                    municipio = :municipio,
                                    pago = :pago
                                    WHERE dni = :dni
                        ''')

                query.bindValue(':dni', cliente.dni)
                query.bindValue(':nombre', cliente.nombre)
                query.bindValue(':alta', cliente.alta)
                query.bindValue(':direccion', cliente.direccion)
                query.bindValue(':provincia', cliente.provincia)
                query.bindValue(':municipio', cliente.municipio)
                query.bindValue(':pago', cliente.pago)

                for coche in cliente.coches:
                    CocheRepository.save(coche)

                for factura in cliente.facturas:
                    FacturaRepository.save(factura)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar un coche en la base de datos: {e}')

    @staticmethod
    def exists(cliente: Cliente) -> bool:
        """

        Informa de existencia de objeto cliente en base de datos

        :param cliente: a encontrar
        :return: si existe
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                        select count(*) 
                                        from clientes
                                        where dni = :id
                        ''')
            query.bindValue(':id', cliente.dni)
            if query.exec():
                while query.next():
                    return query.value(0) > 0
            return False

        except Exception as e:
            print(f'Error al verificar existencia de cliente de la base de datos: {e}')
            return False
