from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QTableWidgetItem

from daos import CocheQtDao
from views import Ui_dlgHistorial


class DlgHistorialController(QDialog):
    def __init__(self):
        super(DlgHistorialController, self).__init__()
        self.ui = Ui_dlgHistorial()
        self.ui.setupUi(self)

        self.load_table_style()
        self.load_table_data()
        self.eneablieBtn()
        self.ui.btnRestaurar.clicked.connect(self.restore_cliente)
        self.ui.btnRestaurar.clicked.connect(self.eneablieBtn)
        self.ui.tabClientes.clicked.connect(self.eneablieBtn)



    def load_table_style(self):
        try:
            # ajuste de tabla a marco
            header = self.ui.tabClientes.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0 or i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            # aplicación de color a tabla
            self.ui.tabClientes.setStyleSheet(
                '''
                QTableView
                {   
                    background-color: white;
                    gridline-color:grey;
                    color: black;
                }
                QTableView::item 
                {   
                    color: black;
                }
                QTableView::item:hover
                {   
                    color: black;
                    background: #ffaa00;            
                }
                QTableView::item:focus
                {   
                    color: black;          
                }
                '''
            )
        except Exception as e:
            print(f'Error al aplicar estilos a la tabla: {e}')

    def load_table_data(self):
        try:
            if len(CocheQtDao.read_bajas()) == 0:
                self.ui.tabClientes.clearContents()
            else:
                coches = CocheQtDao.read_bajas()
                for index, coche in enumerate(coches):
                    self.ui.tabClientes.setRowCount(index + 1)
                    self.ui.tabClientes.setItem(index, 0, QTableWidgetItem(coche.propietario.dni))
                    self.ui.tabClientes.setItem(index, 1, QTableWidgetItem(coche.matricula))
                    self.ui.tabClientes.setItem(index, 2, QTableWidgetItem(coche.marca))
                    self.ui.tabClientes.setItem(index, 3, QTableWidgetItem(coche.modelo))
                    self.ui.tabClientes.setItem(index, 4, QTableWidgetItem(coche.motor))
                    self.ui.tabClientes.setItem(index, 5, QTableWidgetItem(coche.fecha_baja))
        except Exception as e:
            print(f'Error al cargar los datos en la tabla: {e}')

    def restore_cliente(self):
        dni = self.ui.tabClientes.selectedItems()[0].text()
        matricula = self.ui.tabClientes.selectedItems()[1].text()
        CocheQtDao.restore_by_matricula(dni, matricula)
        self.load_table_data()

    def eneablieBtn(self):
        if len(CocheQtDao.read_bajas()) == 0 or not self.ui.tabClientes.selectedItems():
            self.ui.btnRestaurar.setEnabled(False)
        else:
            self.ui.btnRestaurar.setEnabled(True)
