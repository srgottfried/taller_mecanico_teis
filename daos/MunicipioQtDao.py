from PyQt6 import QtSql

from daos import ProvinciaQtDao
from models import Municipio
from services import ConnectionManager


class MunicipioQtDao:
    def __init__(self):
        ConnectionManager().connect()

    @staticmethod
    def read():
        try:
            municipios = []
            query = QtSql.QSqlQuery()
            query.prepare('select id, municipio, provincia_id from municipios')
            if query.exec():
                while query.next():
                    municipio = Municipio(int(query.value(0)), str(query.value(1)))
                    municipios.append(municipio)
            return municipios
        except Exception as e:
            print(f'Error al leer los municipios de la base de datos: {e}')

    @staticmethod
    def read_by_provincia_id(provincia_id):
        try:
            municipios = []
            query = QtSql.QSqlQuery()
            query.prepare('select id, municipio from municipios where provincia_id = :provincia_id')
            query.bindValue(':provincia_id', provincia_id)
            if query.exec():
                while query.next():
                    municipios.append(
                        Municipio(query.value(0),
                                  query.value(1))
                    )
            return municipios
        except Exception as e:
            print(f'Error al leer provincias de la base de datos: {e}')