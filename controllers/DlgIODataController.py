from datetime import datetime

import xlrd
import xlwt
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QDialog, QMessageBox

from controllers import DlgOpenFileController
from models import Cliente
from models.Coche import Coche
from daos import ClienteQtDao, CocheQtDao
from views import Ui_dlgEligeCampos


class DlgIODataController(QDialog):
    """

    Controlador para la transferencia de datos. Gestiona las operaciones de entrada (INPUT) y salida (OUTPUT) de datos
    desde la aplicacion.

    """
    def __init__(self):
        super(DlgIODataController, self).__init__()
        self.ui = Ui_dlgEligeCampos()
        self.ui.setupUi(self)

        self.dlg_open_file = DlgOpenFileController()
        self.coche_dao = CocheQtDao()
        self.cliente_dao = ClienteQtDao()

        self.ui.btnAceptar.clicked.connect(self.export_xml_data)

    def export_xml_data(self):
        """

        Exporta datos a formato XML.

        """
        try:
            export_clientes = self.ui.chkClientes.isChecked()
            export_coches = self.ui.chkCoches.isChecked()

            if not (export_coches or export_clientes):
                pass
            else:
                fecha = datetime.today()
                fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
                file = str(fecha) + '_clientes.xls'
                directorio, filename = self.dlg_open_file.getSaveFileName(None, 'Guardar copia', file, '.xls')

                wb = xlwt.Workbook()

                if export_clientes:
                    sheet1 = wb.add_sheet('Clientes')
                    sheet1.write(0, 0, 'DNI')
                    sheet1.write(0, 1, 'Nombre')
                    sheet1.write(0, 2, 'Fecha de alta')
                    sheet1.write(0, 3, 'Dirección')
                    sheet1.write(0, 4, 'Provincia')
                    sheet1.write(0, 5, 'Municipio')
                    sheet1.write(0, 6, 'Forma de pago')
                    fila = 1
                    query = QSqlQuery()
                    query.prepare('select * from clientes order by dni')
                    if query.exec():
                        while query.next():
                            for i in range(0, 7):
                                sheet1.write(fila, i, str(query.value(i)))
                            fila += 1

                if export_coches:
                    sheet2 = wb.add_sheet('Coches')
                    sheet2.write(0, 0, 'Matrícula')
                    sheet2.write(0, 1, 'DNI cliente')
                    sheet2.write(0, 2, 'Marca')
                    sheet2.write(0, 3, 'Modelo')
                    sheet2.write(0, 4, 'Motor')
                    fila = 1
                    query = QSqlQuery()
                    query.prepare('select * from coches order by matricula')
                    if query.exec():
                        while query.next():
                            for i in range(0, 5):
                                sheet2.write(fila, i, str(query.value(i)))
                            fila += 1

                wb.save(directorio)
                msg = QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText('Exportación de datos realizada')
                msg.exec()

            self.dlg_open_file.close()
            self.close()

        except Exception as error:
            print('Error al exportar datos', error)

    def import_xml_data(self):
        """

        Importa datos en formato XML.

        """
        try:
            filename = self.dlg_open_file.getOpenFileName(None, 'Importar datos', '', 'All Files (*);;zip (*.zip)')
            if self.dlg_open_file.accept and filename != '':
                file = filename[0]
                documento = xlrd.open_workbook(file)
                sheets = documento.sheet_names()
                if 'Clientes' in sheets:
                    datos = documento.sheet_by_name("Clientes")
                    for i in range(datos.nrows):
                        cli = []
                        if i == 0:
                            pass
                        else:
                            for j in range(datos.ncols):
                                cli.append(str(datos.cell_value(i, j)))
                            cl = Cliente(
                                dni=cli[0],
                                nombre=cli[1],
                                alta=cli[2],
                                direccion=cli[3],
                                provincia=cli[4],
                                municipio=cli[5],
                                pago=cli[6])
                            if self.cliente_dao.exists_dni(cli[0]):
                                self.cliente_dao.update(cl)
                            else:
                                self.cliente_dao.create(cl)

                if 'Coches' in sheets:
                    datos = documento.sheet_by_name("Coches")
                    for i in range(datos.nrows):
                        car = []
                        if i == 0:
                            pass
                        else:
                            for j in range(datos.ncols):
                                car.append(str(datos.cell_value(i, j)))
                            if self.cliente_dao.exists_dni(str(car[1])):
                                c = Coche(
                                    matricula=str(car[0]),
                                    marca=str(car[2]),
                                    modelo=str(car[3]),
                                    motor=str(car[4]),
                                    propietario=self.cliente_dao.read(car[1])[0]
                                )
                                if self.coche_dao.exists(c.matricula):
                                    self.coche_dao.update(c)
                                else:
                                    self.coche_dao.create(c)
                    msg = QMessageBox()
                    msg.setModal(True)
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText('Importación de datos realizada con éxito.')
                    msg.exec()

        except Exception as e:
            print(f'Error al importar datos: {e}')

    def export_xml_service_data(self):
        """

        Exporta datos de servicio a formato XML

        """
        try:
            export_servicios = self.ui.chkClientes.isChecked()

            if not export_servicios:
                pass
            else:
                fecha = datetime.today()
                fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
                file = str(fecha) + '_clientes.xls'
                directorio, filename = self.dlg_open_file.getSaveFileName(None, 'Guardar copia', file, '.xls')

                wb = xlwt.Workbook()

                if export_servicios:
                    sheet1 = wb.add_sheet('Servicios')
                    sheet1.write(0, 0, 'CÓDIGO')
                    sheet1.write(0, 1, 'CONCEPTO')
                    sheet1.write(0, 2, 'PRECIO-UNIDAD')
                    fila = 1
                    query = QSqlQuery()
                    query.prepare('select * from servicios order by codigo')
                    if query.exec():
                        while query.next():
                            for i in range(0, 3):
                                sheet1.write(fila, i, str(query.value(i)))
                            fila += 1

                wb.save(directorio)
                msg = QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText('Exportación de SERVICIOS realizada')
                msg.exec()


        except Exception as error:
            print('Error al exportar datos', error)