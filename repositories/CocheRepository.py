from PyQt6 import QtSql

from models import Coche
from services import ConnectionManager


class CocheRepository:
    """

    Clase repositorio encargada de la persistencia de datos asociados a la clae Coche.

    """
    def __init__(self):
        ConnectionManager.connect()

    @staticmethod
    def getAll() -> list[Coche]:
        """

        Obtiene lista de coches de la base de datos.

        :return: list[Coche]
        """
        try:
            coches = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                select matricula, dnicli, marca, modelo, motor, activo, fecha_baja 
                                from coches
                                where activo = 1
                ''')
            if query.exec():
                while query.next():
                    coche = Coche()
                    coche.matricula = query.value(0)
                    coche.propietario_id = query.value(1)
                    coche.marca = query.value(2)
                    coche.modelo = query.value(3)
                    coche.motor = query.value(4)
                    coche.activo = query.value(5)
                    coche.fecha_baja = query.value(6)

                    coches.append(coche)

            return coches

        except Exception as e:
            print(f'Error al leer los coches de la base de datos: {e}')

    @staticmethod
    def getById(id) -> Coche:
        """

        Recupera un objeto coche de la base de datos por id

        :param id: int
        :return: Coche
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select matricula, dnicli, marca, modelo, motor, activo, fecha_baja 
                                    from coches
                                    where activo = 1 and matricula = :id
                    ''')
            query.bindValue(':id', id)
            coche = None
            if query.exec():
                while query.next():
                    coche = Coche()
                    coche.matricula = query.value(0)
                    coche.propietario_id = query.value(1)
                    coche.marca = query.value(2)
                    coche.modelo = query.value(3)
                    coche.motor = query.value(4)
                    coche.activo = query.value(5)
                    coche.fecha_baja = query.value(6)

            return coche

        except Exception as e:
            print(f'Error al leer los coches por ID de la base de datos: {e}')

    @staticmethod
    def getByDni(dni) -> list[Coche]:
        """

        Recupera un objeto de tipo coche por dni de propietario.

        :param dni: del propietario
        :return: lista de coches
        """
        try:
            coches = []
            query = QtSql.QSqlQuery()
            query.prepare('''
                                    select matricula, dnicli, marca, modelo, motor, activo, fecha_baja 
                                    from coches
                                    where activo = 1 and dnicli = :dni
                    ''')
            query.bindValue(':dni', dni)

            if query.exec():
                while query.next():
                    coche = Coche()
                    coche.matricula = query.value(0)
                    coche.propietario_id = query.value(1)
                    coche.marca = query.value(2)
                    coche.modelo = query.value(3)
                    coche.motor = query.value(4)
                    coche.activo = query.value(5)
                    coche.fecha_baja = query.value(6)

                    coches.append(coche)

            return coches

        except Exception as e:
            print(f'Error al leer los coches por DNI de la base de datos: {e}')

    @staticmethod
    def save(coche: Coche):
        """

        Guarda un objeto de tipo coche en la base de datos. Realiza un proceso de persistencia en cascada para los objetos asociados.

        :param coche: a guardar
        :return: si éxito
        """
        if not CocheRepository.exists(coche):
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                    INSERT INTO coches (matricula, dnicli, marca, modelo, motor)
                                    VALUES (:matricula, :dnicli, :marca, :modelo, :motor)
                    ''')

                query.bindValue(':matricula', coche.matricula)
                query.bindValue(':dnicli', coche.propietario_id)
                query.bindValue(':marca', coche.marca)
                query.bindValue(':modelo', coche.modelo)
                query.bindValue(':motor', coche.motor)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar un coche en la base de datos: {e}')
                return False
        else:
            try:
                query = QtSql.QSqlQuery()
                query.prepare('''
                                    UPDATE coches
                                    SET dnicli = :dni, 
                                    marca = :marca,
                                    modelo = :modelo, 
                                    motor = :motor
                                    WHERE matricula = :matricula
                    ''')
                query.bindValue(':matricula', coche.matricula)
                query.bindValue(':dni', coche.propietario_id)
                query.bindValue(':marca', coche.marca)
                query.bindValue(':modelo', coche.modelo)
                query.bindValue(':motor', coche.motor)

                if query.exec():
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error al guardar un coche en la base de datos: {e}')
                return False

    @staticmethod
    def exists(coche: Coche) -> bool:
        """

        Informa de la existencia de objeto de tipo coche en la base de datos.
        Usa implementación de método __eq__ para comparación.

        :param coche: a comparar
        :return: si igual
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                                            select count(*) 
                                            from coches
                                            where matricula = :id
                            ''')
            query.bindValue(':id', coche.matricula)
            if query.exec():
                while query.next():
                    return query.value(0) > 0
            return False

        except Exception as e:
            print(f'Error al verificar existencia de coche de la base de datos: {e}')
            return False