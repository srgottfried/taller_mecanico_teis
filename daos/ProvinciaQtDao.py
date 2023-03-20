from PyQt6 import QtSql

from daos.MunicipioQtDao import MunicipioQtDao
from models import Provincia
from services import ConnectionManager


class ProvinciaQtDao:
    def __init__(self):
        ConnectionManager().connect()

    @staticmethod
    def read():
        try:
            provincias = []
            query = QtSql.QSqlQuery()
            query.prepare('select id, provincia from provincias')
            if query.exec():
                while query.next():
                    provincia = Provincia(
                        int(query.value(0)),
                        str(query.value(1))
                    )
                    provincia.municipios = MunicipioQtDao.read_by_provincia_id(query.value(0))
                    provincias.append(provincia)
            return provincias
        except Exception as e:
            print(f'Error al leer provincias de la base de datos: {e}')
