from PyQt6.QtWidgets import QDialog

from daos import CocheQtDao
from views import Ui_dlgDeleteCliente, Ui_dlgDeleteServicio


class DlgDeleteServicioController(QDialog):
    def __init__(self):
        super(DlgDeleteServicioController, self).__init__()
        self.ui = Ui_dlgDeleteServicio()
        self.ui.setupUi(self)

        self.ui.btnCancelar.clicked.connect(self.close)
        self.ui.btnConfirmar.clicked.connect(self.close)


