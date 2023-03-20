import sys

from PyQt6.QtWidgets import QDialog

from services import ConnectionManager
from views import Ui_dlgSalir


class DlgExitController(QDialog):
    """

    Diálogo de control de cierre seguro de aplicación

    """
    def __init__(self):
        super(DlgExitController, self).__init__()
        self.ui = Ui_dlgSalir()
        self.ui.setupUi(self)

    def exit(self):
        """

        Cierra la aplicación de maenra segura, desconectando el socket de la base de datos.

        """
        try:
            self.show()
            if self.exec():
                ConnectionManager.disconnect()
                sys.exit()
            else:
                self.hide()
        except Exception as error:
            print("Error en función salir %s", error)
