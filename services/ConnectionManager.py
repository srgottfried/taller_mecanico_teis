from PyQt6 import QtSql
from PyQt6.QtWidgets import QMessageBox


class ConnectionManager:
    filedb = 'db/bbdd.sqlite'
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(filedb)

    '''
    Abre una conexión con la base de datos. 
    Si existe una conexión abierta, la utiliza, sin abrir una nueva.
    '''
    @staticmethod
    def connect():
        if ConnectionManager.db.isOpen() and ConnectionManager.db.databaseName() == 'db/bbdd.sqlite':
            return True
        try:
            ConnectionManager.db.open()
            print('Conexión establecida')
            return True
        except Exception as e:
            print(f'Error al establecer conexión con la base de datos {e}')
            QMessageBox.critical(None,
                                 'No se puede abrir la base de datos',
                                 'Conexión no establecida',
                                 QMessageBox.StandardButton.Cancel)
            return False

    '''
    Cierra toda conexión con la base de datos.
    '''
    @staticmethod
    def disconnect():
        if ConnectionManager.db.isOpen():
            try:
                ConnectionManager.db.close()
                print('Conexión cerrada')
            except Exception as e:
                print(f'Error al cerrar la base de datos: {e}')
