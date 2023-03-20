from PyQt6 import QtSql

from models import LineaFactura, Factura
from repositories import ServicioRepository
from services import ConnectionManager


class LineaFacturaRepository:
    """

    Clase repositorio encargada de la persistencia de datos asociados a la clae LineaFactura.
    """
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def getAll() -> list[LineaFactura]:
        """

        Devuelve lista con todas las líneas de factura de la base de datos.

        :return: lista de lineas de factura
        """
        try:
            lineas = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select id, id_factura, id_servicio, unidades 
                                    from lineas_factura
            ''')
            if query.exec():
                while query.next():
                    linea = LineaFactura(servicio=ServicioRepository.getById(query.value(2)),
                                         id_factura=query.value(1))
                    linea.id = query.value(0)
                    linea.unidades = query.value(3)

                    lineas.append(linea)

            return lineas

        except Exception as e:
            print(f'Error al leer las líneas de factura de la base de datos: {e}')

    @staticmethod
    def getByFacturaId(id_factura) -> list[LineaFactura]:
        """

        Retorna lista de lineas de factura por id de factura especificado.

        :param id_factura: a buscar
        :return: lista de lineas de factura correspondientes a la factura de id dado.
        """
        try:
            lineas = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                            select id, id_servicio, unidades 
                                            from lineas_factura
                                            where id_factura = :id_factura
                    ''')
            query.bindValue(':id_factura', id_factura)

            if query.exec():
                while query.next():
                    linea = LineaFactura(servicio=ServicioRepository.getById(query.value(1)),
                                         id_factura=id_factura)
                    linea.id = query.value(0)
                    linea.unidades = query.value(2)

                    lineas.append(linea)

            return lineas

        except Exception as e:
            print(f'Error al leer las línea de factura  por id de factura de la base de datos: {e}')

    @staticmethod
    def getById(id) -> LineaFactura:
        """

        Devuelve linea de factura por id de linea especificado.

        :param id: de linea
        :return: linea de factura por id especificado
        """
        try:
            linea = None
            query = QtSql.QSqlQuery()
            query.prepare('''
                                        select id, id_factura, id_servicio, unidades 
                                        from lineas_factura
                                        where id = :id
                ''')
            query.bindValue(':id', id)

            if query.exec():
                while query.next():
                    linea = LineaFactura(servicio=ServicioRepository.getById(query.value(2)),
                                         id_factura=query.value(1))
                    linea.id = query.value(0)
                    linea.unidades = query.value(3)

            return linea

        except Exception as e:
            print(f'Error al leer la línea de factura  por id de la base de datos: {e}')

    @staticmethod
    def save(linea: LineaFactura) -> bool:
        """

        Guarda linea de factura especificada en base de datos. Propaga en cascada la persistencia de objetos asociados.

        :param linea: de fatctura a almacenar
        :return: si éxito
        """
        if not LineaFacturaRepository.exists(linea):
            try:
                print('nuevo')
                query = QtSql.QSqlQuery()
                query.prepare('''
                                INSERT INTO lineas_factura (id_factura, id_servicio, unidades)
                                VALUES (:id_factura, :id_servicio, :unidades)
                ''')
                query.bindValue(':id_factura', linea.id_factura)
                query.bindValue(':id_servicio', linea.servicio.codigo)
                query.bindValue(':unidades', linea.unidades)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar una línea de factura en la base de datos: {e}')
                return False
        else:
            print('actualiza')
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                UPDATE lineas_factura
                                SET 
                                id_factura = :id_factura, 
                                id_servicio = :id_servicio, 
                                unidades = :unidades
                                WHERE id = :id
                ''')
                query.bindValue(':id', linea.id)
                query.bindValue(':id_factura', linea.id_factura)
                query.bindValue(':id_servicio', linea.servicio.codigo)
                query.bindValue(':unidades', float(linea.unidades))

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar una línea de factura en la base de datos: {e}')
                return False

    @staticmethod
    def remove_by_id(id_linea):
        """

        Borra línea de factura de la base de datos por id de línea. El borrado actua en cascada directa y reflexiva.

        :param id_linea: a borrar
        :return: si éxito
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    delete from lineas_factura
                                    where id = :id_linea
                                ''')
            query.bindValue(':id_linea', id_linea)

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print(f'Error al eliminar una linea de factura de la base de datos: {e}')

    @staticmethod
    def remove(factura: Factura) -> bool:
        """
        Borra línea de factura de la base de datos por objeto. El borrado actua en cascada directa y reflexiva.

        :param factura:
        :return:
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                      delete from lineas_factura
                                      where id_factura = :id      
                            ''')
            query.bindValue(':id', factura.codigo_factura)
            if query.exec():
                return True
            return False

        except Exception as e:
            print(f'Error al borrar linea de factura de la base de datos: {e}')
            return False


    @staticmethod
    def exists(linea: LineaFactura) -> bool:
        """

        Determina la existencia de linea de factura pasada por parámetro.

        :param linea: a confirmar existencia
        :return: si existe
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                        select count(*) 
                                        from lineas_factura
                                        where id = :id
                        ''')
            query.bindValue(':id', linea.id)
            if query.exec():
                while query.next():
                    return query.value(0) > 0
            return False

        except Exception as e:
            print(f'Error al verificar existencia de linea de factura de la base de datos: {e}')
            return False
