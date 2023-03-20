from PyQt6.QtWidgets import QDialog

from views import Ui_dlgDeleteFactura


class DlgDeleteFacturaController(QDialog):
    def __init__(self):
        super(DlgDeleteFacturaController, self).__init__()
        self.ui = Ui_dlgDeleteFactura()
        self.ui.setupUi(self)

        self.ui.btnCancelar.clicked.connect(self.close)
        self.ui.btnConfirmar.clicked.connect(self.close)
