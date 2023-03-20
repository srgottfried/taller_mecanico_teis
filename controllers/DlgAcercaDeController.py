import sys

from PyQt6.QtWidgets import QDialog

from views import Ui_dlgAcercaDe


class DlgAcercaDeController(QDialog):
    """

    Diálogo de control de cierre seguro de aplicación

    """
    def __init__(self):
        super(DlgAcercaDeController, self).__init__()
        self.ui = Ui_dlgAcercaDe()
        self.ui.setupUi(self)

        self.ui.btnVolver.clicked.connect(self.close)
