from PyQt6 import QtSql

from models import Factura
from repositories import LineaFacturaRepository
from services import ConnectionManager


class FacturaRepository:
    """
    Clase repositorio encargada de la persistencia de datos asociados a la clae Factura.
    """
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def getAll() -> list[Factura]:
        """

        Obtiene lista de facturas de la base de datos.

        :return: list[Factura]
        """
        try:
            facturas = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select codigo, cliente_id, fecha, matricula, emitida, descuento 
                                from facturas
                ''')
            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.id_cliente = query.value(1)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    factura.emitida = query.value(4)
                    factura.descuento = query.value(5)

                    factura.add_lineas_de_factura(LineaFacturaRepository.getByFacturaId(factura.codigo_factura))
                    facturas.append(factura)

            return facturas

        except Exception as e:
            print(f'Error al leer las facturas de la base de datos: {e}')

    @staticmethod
    def getById(id) -> Factura:
        """

        Recupera un objeto factura de la base de datos por id de factura

        :param id: int
        :return: Factura
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select codigo, cliente_id, fecha, matricula, emitida, descuento 
                                    from facturas
                                    where codigo = :id
                    ''')
            query.bindValue(':id', id)

            factura = None

            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.id_cliente = query.value(1)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    factura.emitida = query.value(4)
                    factura.descuento = query.value(5)
                    factura.add_lineas_de_factura(LineaFacturaRepository.getByFacturaId(factura.codigo_factura))

            return factura

        except Exception as e:
            print(f'Error al leer la factura por id de la base de datos: {e}')

    @staticmethod
    def getByClienteId(id) -> list[Factura]:
        """

        Obtiene una lista de objetos factura a partir del id del cliente de la factura.

        :param id: del cliente
        :return: lista de facturas
        """

        try:
            facturas = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select codigo, cliente_id, fecha, matricula, emitida, descuento 
                                from facturas
                                where cliente_id = :id
                    ''')
            query.bindValue(':id', id)

            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.id_cliente = query.value(1)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    factura.emitida = query.value(4)
                    factura.descuento = query.value(5)
                    factura.add_lineas_de_factura(LineaFacturaRepository.getByFacturaId(factura.codigo_factura))
                    facturas.append(factura)

            return facturas

        except Exception as e:
            print(f'Error al leer las facturas de la base de datos: {e}')

    @staticmethod
    def getByMatricula(matricula) -> list[Factura]:
        """

        Obtiene una lista de objetos factura a partir de la matrícula asociada

        :param matricula: asociada a la factura
        :return: lista de matrículas
        """
        try:
            facturas = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                        select codigo, cliente_id, fecha, matricula, emitida, descuento 
                                        from facturas
                                        where matricula = :matricula
                        ''')
            query.bindValue(':matricula', matricula)

            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.id_cliente = query.value(1)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    factura.emitida = query.value(4)
                    factura.descuento = query.value(5)
                    factura.add_lineas_de_factura(LineaFacturaRepository.getByFacturaId(factura.codigo_factura))

                    facturas.append(factura)

            return facturas

        except Exception as e:
            print(f'Error al leer las facturas por matrícula de la base de datos: {e}')

    @staticmethod
    def save(factura: Factura):
        """

        Guarda un objeto factura en la base de datos. Aplica persistencia en cascada para los objetos asociados.

        :param factura: objeto a guardar
        :return: None
        """
        if not FacturaRepository.exists(factura):
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                INSERT INTO facturas (cliente_id, fecha, matricula, emitida, descuento)
                                VALUES (:cliente_id, :fecha, :matricula, :emitida, :descuento)
                ''')
                query.bindValue(':cliente_id', factura.id_cliente)
                query.bindValue(':fecha', factura.fecha)
                query.bindValue(':matricula', factura.matricula)
                query.bindValue(':emitida', factura.emitida)
                query.bindValue(':descuento', factura.descuento)

                if factura.lineas_de_factura is not []:
                    for linea in factura.lineas_de_factura:
                        LineaFacturaRepository.save(linea)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar una factura en la base de datos: {e}')
                return False
        else:
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                UPDATE facturas 
                                SET cliente_id = :cliente_id,
                                fecha = :fecha, 
                                matricula = :matricula,
                                emitida = :emitida,
                                descuento = :descuento
                                WHERE codigo = :codigo
                ''')
                query.bindValue(':codigo', int(factura.codigo_factura))
                query.bindValue(':cliente_id', factura.id_cliente)
                query.bindValue(':fecha', factura.fecha)
                query.bindValue(':matricula', factura.matricula)
                query.bindValue(':emitida', factura.emitida)
                query.bindValue(':descuento', factura.descuento)

                if factura.lineas_de_factura is not []:
                    for linea in factura.lineas_de_factura:
                        LineaFacturaRepository.save(linea)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar una factura en la base de datos: {e}')
                return False

    @staticmethod
    def getLastInsert() -> Factura:
        """

        Retorna la última factura insertada en la base de datos.

        :return: objeto factura
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select codigo, cliente_id, fecha, matricula, emitida, descuento 
                                    from facturas
                                    where codigo = (select max(codigo) from facturas)
                            ''')
            factura = None
            if query.exec():
                while query.next():
                    factura = Factura()
                    factura.codigo_factura = query.value(0)
                    factura.id_cliente = query.value(1)
                    factura.fecha = query.value(2)
                    factura.matricula = query.value(3)
                    factura.emitida = query.value(4)
                    factura.descuento = query.value(5)

            return factura

        except Exception as e:
            print(f'Error al obtener la última inserción de la base de datos: {e}')
            return False

    @staticmethod
    def remove(factura: Factura) -> bool:
        """

        Elimina el objeto factura de la base de datos. Elimina en cascada todos los objetos asociados.

        :param factura: factura a eliminar.
        :return: Booleano
        """
        try:
            LineaFacturaRepository.remove(factura)
            query = QtSql.QSqlQuery()
            query.prepare('''
                                                delete from facturas
                                                where codigo = :id
                                ''')
            query.bindValue(':id', factura.codigo_factura)
            if query.exec():
                return True
            return False

        except Exception as e:
            print(f'Error al verificar existencia de factura de la base de datos: {e}')
            return False

    @staticmethod
    def exists(factura: Factura) -> bool:
        """

        Retorna la existencia de una factura pasada por parámetro.

        :param factura: para comprobar existencia
        :return: Boolean
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                            select count(*) 
                                            from facturas
                                            where codigo = :id
                            ''')
            query.bindValue(':id', factura.codigo_factura)
            if query.exec():
                while query.next():
                    return query.value(0) > 0
            return False

        except Exception as e:
            print(f'Error al verificar existencia de factura de la base de datos: {e}')
            return False