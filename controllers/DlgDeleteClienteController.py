from PyQt6.QtWidgets import QDialog

from daos import CocheQtDao
from views import Ui_dlgDeleteCliente


class DlgDeleteClienteController(QDialog):
    def __init__(self):
        super(DlgDeleteClienteController, self).__init__()
        self.ui = Ui_dlgDeleteCliente()
        self.ui.setupUi(self)

        self.ui.btnCancelar.clicked.connect(self.close)
        self.ui.btnConfirmar.clicked.connect(self.close)

    def load_client_data(self, dni, nombre):
        """

        Carga datos del cliente seleccionado, tomando dni y nombre como datos de referencia.

        :param dni: del cliente
        :param nombre: del cliente
        """
        self.ui.lblDni.setText(f'DNI:  {dni}')
        num_coches = len(CocheQtDao.read_altas(dni))
        self.ui.lblNombre.setText(f'Nombre:  {nombre}')
        self.ui.lblNumCoches.setText(f'Número de coches en taller:  {num_coches}')
