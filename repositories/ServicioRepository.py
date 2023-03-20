from PyQt6 import QtSql

from models import Servicio
from services import ConnectionManager


class ServicioRepository:
    """

    Clase repositorio encargada de la persistencia de datos asociados a la clae Servicio.
    """
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def getAll() -> list[Servicio]:
        """

        Obtiene lista de todos los servicios de la base de datos.

        :return: Lista de servicios de la base de datos
        """
        try:
            servicios = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select codigo, concepto, "precio-unidad", stock 
                                    from servicios
            ''')
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
    def getById(id) -> Servicio:
        """

        Obtiene servicio por id de servicio

        :param id: de servicio
        :return: servicio buscado por id
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select codigo, concepto, "precio-unidad", stock 
                                from servicios 
                                where codigo = :id
            ''')
            query.bindValue(':id', id)
            serv = None
            if query.exec():
                while query.next():
                    serv = Servicio()
                    serv.codigo = query.value(0)
                    serv.concepto = query.value(1)
                    serv.precio_unidad = query.value(2)
                    serv.stock = query.value(3)
            return serv

        except Exception as e:
            print(f'Error al leer los servicios de la base de datos: {e}')

    @staticmethod
    def save(servicio: Servicio) -> bool:
        """

        Guarda servicio en base de datos. Persiste en cascada todos los objetos asociados al objeto servicio.

        :param servicio: a persistir
        :return: si éxito
        """
        if not ServicioRepository.exists(servicio):
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                        insert into servicios (concepto, "precio-unidad", stock) 
                                        values (:concepto, :precio, :stock)
                ''')
                query.bindValue(':concepto', servicio.concepto)
                query.bindValue(':precio', servicio.precio_unidad)
                query.bindValue(':stock', servicio.stock)

                if query.exec():
                    return True
                else:
                    return False
            except Exception as e:
                print(f'Error al insertar un nuevo servicio en la base de datos: {e}')
        else:
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

    @staticmethod
    def remove(id) -> bool:
        """

        Borra servicio por id

        :param id: de servicio
        :return: si éxito
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    delete from servicios 
                                    where codigo = :codigo
            ''')
            query.bindValue(':codigo', str(id))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al borrar un servicio de la base de datos: {e}')

    @staticmethod
    def exists(servicio: Servicio) -> bool:
        """

        Informa de la existenica de Servicio en la base de datos.

        :param servicio: buscado
        :return: si exite
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                            select count(*) 
                                            from servicios
                                            where codigo = :id
                            ''')
            query.bindValue(':id', servicio.codigo)
            if query.exec():
                while query.next():
                    return query.value(0) > 0
            return False

        except Exception as e:
            print(f'Error al verificar existencia de servicio de la base de datos: {e}')
            return False
