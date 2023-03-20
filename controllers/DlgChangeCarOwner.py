from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QTableWidgetItem

from controllers import DlgCalendarController
from daos import ProvinciaQtDao, ClienteQtDao, CocheQtDao
from models import Cliente
from services import DniManager
from views import Ui_dlgChangeCarOwner


class DlgChangeCarOwner(QDialog):
    def __init__(self):
        super(DlgChangeCarOwner, self).__init__()
        self.ui = Ui_dlgChangeCarOwner()
        self.ui.setupUi(self)

        # Daos
        self.provincias_dao = ProvinciaQtDao()
        self.clientes_dao = ClienteQtDao()
        self.coche_dao = CocheQtDao()

        # Dlgs
        self.dlg_calendar = DlgCalendarController()

        # Signals
        self.ui.btnCancelar.clicked.connect(self.close)
        self.ui.txtDniCli.editingFinished.connect(self.dni_validator)
        self.ui.btnFechaAltaCli.clicked.connect(self.dlg_calendar.show)
        self.dlg_calendar.ui.Calendar.clicked.connect(self.load_date)

        # Load data
        self.load_provincias()
        self.ui.cmbProCli.currentIndexChanged.connect(self.load_municipios)
        self.load_clientes_list()
        self.load_table_data()
        self.ui.cmbCli.currentIndexChanged.connect(self.load_client)
        self.ui.tabClientes.clicked.connect(self.load_ficha)

        self.ui.btnConfirmar.clicked.connect(self.confirmar)
        self.ui.txtNombreCli.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtDirCli.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.btnConfirmar.setEnabled(False)
        self.ui.tabClientes.clicked.connect(self.eneableBtns)
        self.ui.txtDniCli.editingFinished.connect(self.eneableBtns)
        self.ui.txtDirCli.editingFinished.connect(self.eneableBtns)
        self.ui.txtNombreCli.editingFinished.connect(self.eneableBtns)
        self.ui.txtFechaAltaCli.editingFinished.connect(self.eneableBtns)
        self.ui.chkEfectivo.clicked.connect(self.eneableBtns)
        self.ui.chkTarjeta.clicked.connect(self.eneableBtns)
        self.ui.chkTransferencia.clicked.connect(self.eneableBtns)
        self.ui.cmbCli.currentIndexChanged.connect(self.eneableBtns)

        # Carga de estilos
        self.load_table_style()
        self.ui.cmbCli.currentIndexChanged.connect(self.dni_validator)

    def eneableBtns(self):
        """

        Activa botonera en itneracción con usuario para mejorar experiencia de uso.

        """
        try:
            if not self.ui.tabClientes.selectedItems() or self.ui.txtDniCli.text() == '' or not DniManager.validate_dni(
                    self.ui.txtDniCli.text()):
                self.ui.btnConfirmar.setEnabled(False)
            else:
                self.ui.btnConfirmar.setEnabled(True)


        except Exception as e:
            print('Error al activar botones')

    def confirmar(self):
        """

        Evento asociado al botón de confirmación de cambio de propietario del coche

        """
        matricula_coche = self.ui.tabClientes.selectedItems()[1].text()
        datos = self.read_interface()
        try:
            if ClienteQtDao.exists_dni(datos['dni']):
                CocheQtDao.change_owner(matricula_coche, datos['dni'])
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Confirmacion')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('El propietario se ha actualizado con éxito.')
                msg.exec()
            else:
                if datos['dni'] == '' or datos['nombre'] == '' or datos['fecha_alta'] == '' or datos[
                    'formas_pago'] == '':
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('Deben cubrirse los campos obligatorios.')
                    msg.exec()
                elif not DniManager.validate_dni(datos['dni']):
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('DNI inválido.')
                    msg.exec()
                else:
                    cliente = Cliente(datos['dni'],
                                      datos['nombre'],
                                      datos['fecha_alta'],
                                      datos['direccion'],
                                      datos['provincia'],
                                      datos['municipio'],
                                      datos['formas_pago'])

                    ClienteQtDao.create(cliente)
                    CocheQtDao.change_owner(matricula_coche, datos['dni'])
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Confirmación')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('El propietario se ha creado y actualizado con éxito.')
                    msg.exec()

            self.load_table_data()
        except Exception as e:
            print(f'Error al confirmar cambio de propietario: {e}')

    def text_lbl_to_mayus(self):
        """

        Conversor de cadenas de caracteres a formato específico.

        """
        try:
            self.ui.txtNombreCli.setText(self.ui.txtNombreCli.text().title())
            self.ui.txtDirCli.setText(self.ui.txtDirCli.text().title())
        except Exception as error:
            print("Error al procesar las letras capitales", error)

    def dni_validator(self):
        """

        Validador de dni segun reglas de formación de la legislación española.
        Basado en el algoritmo de determinación para DNI localizados y nacionales.

        """
        try:
            dni = self.ui.txtDniCli.text()
            if DniManager.validate_dni(dni):
                self.ui.lblValidarDNI.setStyleSheet("color:green")
                self.ui.lblValidarDNI.setText('V')
                self.ui.txtDniCli.setText(dni.upper())
                self.ui.txtDniCli.setStyleSheet("background-color: none")
            else:
                self.ui.lblValidarDNI.setStyleSheet("color:red")
                self.ui.lblValidarDNI.setText('X')
                self.ui.txtDniCli.setText(dni.upper())
                self.ui.txtDniCli.setStyleSheet("background-color: #F64E4E")
        except Exception as error:
            print("Error al mostrar marcador validez dni: ", error)

    def read_interface(self):
        """

        Lectura de datos de la interfaz gráfica asociada a la gestión de propietarios de coches.

        :return: datos de propietario
        """
        try:
            formas_pago = ''
            if self.ui.chkEfectivo.isChecked():
                formas_pago = formas_pago + 'efectivo;'
            if self.ui.chkTarjeta.isChecked():
                formas_pago = formas_pago + 'tarjeta;'
            if self.ui.chkTransferencia.isChecked():
                formas_pago = formas_pago + 'transferencia;'
            return {
                'dni': self.ui.txtDniCli.text(),
                'nombre': self.ui.txtNombreCli.text(),
                'fecha_alta': self.ui.txtFechaAltaCli.text(),
                'direccion': self.ui.txtDirCli.text(),
                'provincia': self.ui.cmbProCli.currentText(),
                'municipio': self.ui.cmbMuniCli.currentText(),
                'formas_pago': formas_pago}
        except Exception as e:
            print(f'Error al leer la interface: {e}')

    def load_ficha(self):
        """

        Evento de carga de ficha de de coche asociado.

        """
        try:
            dni = self.ui.tabClientes.selectedItems()[0].text()
            cliente: Cliente = ClienteQtDao.read(dni)[0]
            direccion = cliente.direccion + ', ' + cliente.provincia
            self.ui.lblNombreFicha.setText('Nombre:  ' + cliente.nombre)
            self.ui.lblDniFicha.setText('DNI:  ' + cliente.dni)
            self.ui.lblDireccionFicha.setText('Dirección:  ' + direccion);
        except Exception as e:
            print(f'Error al recuperar la ficha del usuario: {e}')

    def load_client(self):
        """

        Evento de carga de cliente.

        :return:
        """

        try:
            cliente: Cliente = self.ui.cmbCli.currentData()
            self.ui.txtNombreCli.setText(cliente.nombre)
            self.ui.txtDniCli.setText(cliente.dni)
            self.ui.txtDirCli.setText(cliente.direccion)
            self.ui.txtFechaAltaCli.setText(cliente.alta)
            self.ui.cmbMuniCli.setCurrentText(cliente.municipio)
            self.ui.cmbProCli.setCurrentText(cliente.provincia)
            if 'tarjeta' in cliente.pago:
                self.ui.chkTarjeta.setChecked(True)
            if 'efectivo' in cliente.pago:
                self.ui.chkEfectivo.setChecked(True)
            if 'transferencia' in cliente.pago:
                self.ui.chkTransferencia.setChecked(True)
        except Exception as e:
            pass

    def load_clientes_list(self):
        """

        Evento de carga de lista de clientes.

        """
        self.ui.cmbCli.clear()
        try:
            clientes = self.clientes_dao.readAll()
            self.ui.cmbCli.addItem('')
            for c in clientes:
                input = c.nombre + ' - [' + c.dni + ']'
                self.ui.cmbCli.addItem(input, c)
        except Exception as e:
            print(f'Error al cargar clientes en el buscador de clientes: {e}')

    def load_date(self, qDate):
        """

        Evento de carga de fecha por el horario internacional UTC a región específica.

        :param qDate:
        """
        try:
            data = ("{0}/{1}/{2}".format(qDate.day(), qDate.month(), qDate.year()))
            self.ui.txtFechaAltaCli.setText(data)
            self.dlg_calendar.hide()
        except Exception as e:
            print(f'Error al cargar la fecha de alta: {e}')

    def load_table_style(self):
        """

        Carga de estilos de tabla.

        """
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
        """

        Evento de carga de datos de tabla

        """
        try:
            coches = self.coche_dao.read()
            if len(coches) == 0:
                self.ui.tabClientes.clearContents()
            else:
                for index, coche in enumerate(coches):
                    self.ui.tabClientes.setRowCount(index + 1)
                    self.ui.tabClientes.setItem(index, 0, QTableWidgetItem(coche.propietario.dni))
                    self.ui.tabClientes.setItem(index, 1, QTableWidgetItem(coche.matricula))
                    self.ui.tabClientes.setItem(index, 2, QTableWidgetItem(coche.marca))
                    self.ui.tabClientes.setItem(index, 3, QTableWidgetItem(coche.modelo))
                    self.ui.tabClientes.setItem(index, 4, QTableWidgetItem(coche.motor))
        except Exception as e:
            print(f'Error al cargar los datos en la tabla: {e}')

    def load_provincias(self):
        """

        Evento de carga de provincias de la base de datos.

        """
        try:
            self.ui.cmbProCli.addItem('')
            provincias = self.provincias_dao.read()
            for p in provincias:
                self.ui.cmbProCli.addItem(p.nombre, p)
        except Exception as e:
            print(f'Error al cargar las provincias: {e}')

    def load_municipios(self):
        """

        Evento de carga de municipios de la base de datos.

        """
        try:
            self.ui.cmbMuniCli.clear()
            cd = self.ui.cmbProCli.currentData()
            if cd is not None:
                for muni in cd.municipios:
                    self.ui.cmbMuniCli.addItem(muni.nombre, muni)
        except Exception as e:
            print(f'Error al cargar los municipios: {e}')
