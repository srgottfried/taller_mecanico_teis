# Clase controladora de la ventana principal.
# Carga su vista correspondiente y despliega el sistema de señales de Qt para la ventana principal.

import os, re
import shutil
import zipfile
from datetime import datetime, date
from functools import partial

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget, QComboBox, QPushButton, QLineEdit
from models import Servicio, LineaFactura, Factura
from models.Cliente import Cliente
from models.Coche import Coche
from daos import *
import views
from controllers import *
from repositories import ServicioRepository, LineaFacturaRepository, FacturaRepository, CocheRepository, \
    ClienteRepository
from services import ConnectionManager, DniManager
from services.Informe import Informe


class MainWindowController(QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()

        # Variable de acceso a widgets y carga de vista en controlador
        self.view_holder = {}
        self.txt_eliminar = None
        self.txt_subtotal = None
        self.txt_precio = None
        self.txt_unidades = None
        self.cmb_servicio = None
        self.ui = views.Ui_mainWindow()
        self.ui.setupUi(self)
        self.modifing = False
        self.ui.btnEliminarCli.setEnabled(False)
        self.ui.btnModifCli.setEnabled(False)
        self.ui.btnModifServicio.setEnabled(False)
        self.ui.lbl_factura_emitida.setVisible(False)
        self.ui.lbl_factura_emitida_desc.setVisible(False)
        self.ui.etDescuento.setEnabled(False)
        self.ui.btnAplicarDescuento.setEnabled(False)

        self.ui.btnImprimirFactura.setEnabled(False)
        self.ui.btnBajaFactura.setEnabled(False)

        # Conexión con la base de datos
        ConnectionManager.connect()
        # daos
        self.cliente_dao = ClienteQtDao()
        self.coche_dao = CocheQtDao()
        self.provincias_dao = ProvinciaQtDao()
        self.servicios_dao = ServicioQtDao()

        # Instancias de controladores
        self.dlg_calendar = DlgCalendarController()
        self.dlg_exit = DlgExitController()
        self.dlg_open_file = DlgOpenFileController()
        self.dlg_io_data = DlgIODataController()
        self.dlg_historial = DlgHistorialController()
        self.dlg_del_client = DlgDeleteClienteController()
        self.dlg_change_owner = DlgChangeCarOwner()
        self.dlg_delete_service = DlgDeleteServicioController()
        self.dlg_delete_factura = DlgDeleteFacturaController()
        self.dlg_acerca_de = DlgAcercaDeController()

        # Carga de datos
        self.load_table_data()
        self.load_table_services_data()
        self.load_provincias()

        # Carga de estilos
        self.load_table_style()
        self.load_table_services_style()
        self.load_table_facturas_style()
        # self.load_table_ventas_style()

        ################# SERVICIOS ###################

        self.ui.tabServicios.clicked.connect(self.loadTempService)
        self.ui.btnGuardapServicio.clicked.connect(self.add_service)
        self.ui.tabServicios.clicked.connect(self.load_selected_service_data)
        self.ui.btnEliminarServicio.clicked.connect(self.delete_service)
        self.ui.btnModifServicio.clicked.connect(self.update_service)
        ###############################################

        # Señales:
        #   calendario
        self.ui.btnFechaAltaCli.clicked.connect(self.dlg_calendar.show)
        self.dlg_calendar.ui.Calendar.clicked.connect(self.load_date)
        #   salir
        self.ui.actionSalir.triggered.connect(self.dlg_exit.exit)
        self.ui.actionSalirBar.triggered.connect(self.dlg_exit.exit)
        #   combo-box provincias
        self.ui.cmbProCli.currentIndexChanged.connect(self.load_municipios)
        self.ui.btnGuardaCli.clicked.connect(self.save_cliente)
        #   datos interfaz
        self.ui.btnLimpiarCli.clicked.connect(self.clear_ui)
        self.ui.tabClientes.clicked.connect(self.load_selected_data)
        self.ui.txtDniCli.editingFinished.connect(self.dni_validator)
        self.ui.tabClientes.clicked.connect(self.dni_validator)
        self.ui.txtNombreCli.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtMarca.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtMatricula.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtDirCli.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtModelo.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtPrecioServicio.editingFinished.connect(self.text_lbl_to_mayus)
        self.ui.txtConceptoServicio.editingFinished.connect(self.text_lbl_to_mayus)

        # INFORMES
        self.informes = Informe()
        self.ui.actionInformes_de_clientes.triggered.connect(self.informes.list_clientes)
        self.ui.actionInforme_de_coches.triggered.connect(self.informes.list_autos)
        self.ui.actionInforme_servicio.triggered.connect(self.informes.list_servicios)

        #   backups DB
        self.ui.actionpushDB.triggered.connect(self.create_backup)
        self.ui.actionCrear_copia_de_seguridad.triggered.connect(self.create_backup)
        self.ui.actionpullDB.triggered.connect(self.restore_backup)
        self.ui.actionRestaurar_copia_de_seguridad.triggered.connect(self.restore_backup)
        #   backups data
        self.ui.actionExportar_datos.triggered.connect(self.dlg_io_data.show)
        self.ui.actionactionpushFILE.triggered.connect(self.dlg_io_data.show)
        self.ui.actionImportar_datos.triggered.connect(self.dlg_io_data.import_xml_data)
        self.ui.actionactionpullFILE.triggered.connect(self.dlg_io_data.import_xml_data)
        #   botonera
        self.ui.btnEliminarCli.clicked.connect(self.dlg_del_client.show)
        self.dlg_del_client.ui.btnConfirmar.clicked.connect(self.delete_cliente)
        self.ui.btnModifCli.clicked.connect(self.modify_data)
        self.ui.actionactionHistorico.triggered.connect(self.dlg_historial.show)
        self.ui.actionactionHistorico.triggered.connect(self.dlg_historial.eneablieBtn)
        self.ui.actionModificarPropietario.triggered.connect(self.dlg_change_owner.show)
        self.ui.actionModificarPropietario.triggered.connect(self.dlg_change_owner.load_clientes_list)
        self.ui.actionModificarPropietario.triggered.connect(self.dlg_change_owner.load_table_data)
        self.ui.actionAcerca_de.triggered.connect(self.dlg_acerca_de_show)

        self.ui.tabClientes.clicked.connect(self.eneableBtns)
        self.ui.btnModifCli.clicked.connect(self.eneableBtns)
        self.ui.btnEliminarCli.clicked.connect(self.eneableBtns)
        self.dlg_del_client.ui.btnConfirmar.clicked.connect(self.clear_ui)
        self.dlg_del_client.ui.btnConfirmar.clicked.connect(self.eneableBtns)
        self.ui.btnLimpiarCli.clicked.connect(self.eneableBtns)
        self.ui.tabServicios.clicked.connect(self.eneableButt)

        #   load table data
        self.ui.btnGuardaCli.clicked.connect(self.load_table_data)
        self.ui.actionImportar_datos.triggered.connect(self.load_table_data)
        self.ui.actionpullDB.triggered.connect(self.load_table_data)
        self.ui.actionactionpullFILE.triggered.connect(self.load_table_data)
        self.ui.actionImportar_datos.triggered.connect(self.load_table_data)
        self.ui.actionpullDB.triggered.connect(self.load_table_data)
        self.ui.actionRestaurar_copia_de_seguridad.triggered.connect(self.load_table_data)
        self.dlg_historial.ui.btnRestaurar.clicked.connect(self.load_table_data)
        self.dlg_change_owner.ui.btnConfirmar.clicked.connect(self.load_table_data)
        self.ui.btnGuardapServicio.clicked.connect(self.load_table_services_data)
        self.ui.btnModifServicio.clicked.connect(self.load_table_services_data)
        self.ui.btnEliminarServicio.clicked.connect(self.load_table_services_data)
        self.ui.actionExportar_servicios.triggered.connect(self.dlg_io_data.export_xml_service_data)
        self.ui.tabServicios.clicked.connect(self.text_lbl_to_mayus)

        ######################################################
        #   pestana facturacion
        ######################################################

        # Cargando datos facturacion
        self.load_table_facturas_data()
        self.ui.btnEmitirFactura.setEnabled(False)

        # Eventos pestaña facturacion
        self.ui.tabClientes.clicked.connect(self.load_datos_cliente_en_factura)
        self.ui.btnImprimirFactura.clicked.connect(partial(self.informes.list_facturas, self.ui.txtNumFactura))
        self.ui.tab_facturas.itemSelectionChanged.connect(self.load_lineas_factura_en_tab_ventas)
        self.ui.tab_facturas.itemSelectionChanged.connect(self.generar_nueva_linea_venta)
        self.ui.tab_facturas.itemSelectionChanged.connect(self.descontar)
        self.ui.btnRecargarFactura.clicked.connect(self.load_table_facturas_data)
        self.ui.btnBuscarFactura.clicked.connect(self.buscar_factura)
        self.ui.btnAltaFactura.clicked.connect(self.alta_factura)
        self.ui.btnEmitirFactura.clicked.connect(self.emitir_factura)
        self.ui.btnEmitirFactura.clicked.connect(self.descontar)
        self.ui.btnBajaFactura.clicked.connect(self.delete_factura)
        self.ui.btnBuscarServicio.clicked.connect(self.buscar_servicio)
        self.ui.btnRecargarServicios.clicked.connect(self.load_table_services_data)
        self.ui.btnBuscarCli.clicked.connect(self.buscar_cliente)
        self.ui.btnRecargarClientes.clicked.connect(self.load_table_data)

        self.ui.btnAplicarDescuento.clicked.connect(self.descontar)



    def descontar(self):
        try:

            descuento_porciento = int(self.ui.etDescuento.text())
            subtotal = float(self.ui.txtSubtotal.text())

            descuento_num = float(subtotal * descuento_porciento / 100)

            nuevo_subtotal = subtotal - descuento_num

            nuevo_total = nuevo_subtotal * 1.21




            factura = FacturaRepository.getById(int(self.ui.txtNumFactura.text()))

            factura.descuento = descuento_porciento

            FacturaRepository.save(factura)

            self.ui.txtDescuento.setText('{:.2f}'.format(descuento_num))
            self.ui.txtTotal.setText('{:.2f}'.format(nuevo_total))

        except Exception as e:
            print('Error al aplicar el descuento: ', e)

    def dlg_acerca_de_show(self):
        self.dlg_acerca_de.show()

    def buscar_cliente(self):
        try:
            id = self.ui.txtDniCli.text()
            coches = CocheRepository.getByDni(id)
            self.ui.tabClientes.clearContents()

            for index, coche in enumerate(coches):
                self.ui.tabClientes.setRowCount(index + 1)
                self.ui.tabClientes.setItem(index, 0, QTableWidgetItem(coche.propietario_id))
                self.ui.tabClientes.setItem(index, 1, QTableWidgetItem(coche.matricula))
                self.ui.tabClientes.setItem(index, 2, QTableWidgetItem(coche.marca))
                self.ui.tabClientes.setItem(index, 3, QTableWidgetItem(coche.modelo))
                self.ui.tabClientes.setItem(index, 4, QTableWidgetItem(coche.motor))

        except Exception as e:
            self.ui.tabClientes.clearContents()
            print('Error al buscar cliente:' ,e)


    def buscar_servicio(self):
        try:
            id = self.ui.txtBuscadorServicios.text()
            serv = ServicioRepository.getById(int(id))
            self.ui.tabServicios.clearContents()

            index = 0
            self.ui.tabServicios.setRowCount(index + 1)
            self.ui.tabServicios.setItem(index, 0, QTableWidgetItem(str(serv.codigo)))
            self.ui.tabServicios.setItem(index, 1, QTableWidgetItem(str(serv.concepto).title()))
            self.ui.tabServicios.setItem(index, 2, QTableWidgetItem(serv.precio_unidad))
            self.ui.tabServicios.setItem(index, 3, QTableWidgetItem(str(serv.stock)))

        except Exception as e:
            print('Servicio no encontrado', e)
            self.ui.tabServicios.clearContents()

    def delete_factura_confirm(self):
        self.baja_factura()

    def delete_factura(self):
        try:
            self.dlg_delete_factura.show()
            self.dlg_delete_factura.ui.btnConfirmar.clicked.connect(self.delete_factura_confirm)
        except Exception as e:
            print('Error al borrar factura', e)

    def emitir_factura(self):
        """

        Emite una factura en estado provisional, impidiendo su posterior modificación.

        """
        try:
            factura = FacturaRepository.getById(int(self.ui.txtNumFactura.text()))
            factura.emitir_factura()
            FacturaRepository.save(factura)

            self.load_lineas_factura_en_tab_ventas()

            for serv in factura.lineas_de_factura:
                servicio = ServicioRepository.getById(serv.servicio.codigo)
                servicio.stock = servicio.stock - serv.unidades

                ServicioRepository.save(servicio)


            self.load_table_services_data()

        except Exception as e:
            print(e)

    def generador_escuchadores_view_holder(self):
        """

        Genera escuchadores de manera dinámica para las vistas asociadas al view holder

        """
        try:
            for k in self.view_holder:
                line = self.view_holder[k]
                # k -> id de la linea
                # line -> array estático con los objetos (vistas) de la linea

                # combobox
                cmb_concepto: QComboBox = line[0]
                cmb_concepto.currentIndexChanged.connect(partial(self.actualizar_cmb_linea_factura, k))

                # unidades
                txt_unidades: QLineEdit = line[2]
                txt_unidades.editingFinished.connect(partial(self.actualizar_unidades_linea_factura, k))

                # botón eliminar de linea de factura
                btn_eliminar_linea: QPushButton = line[4]
                btn_eliminar_linea.clicked.connect(partial(self.eliminar_linea_factura, k))

        except Exception as e:
            print(e)

    def actualizar_unidades_linea_factura(self, id_linea):
        """

        Evento asociado al escuchador vinculado al QLineEdit de unidades en la línea de factura.

        :param id_linea: linea de factura a modificar
        """
        try:
            line = self.view_holder.get(id_linea)
            txt_unidades: QLineEdit = line[2]

            linea: LineaFactura = LineaFacturaRepository.getById(id_linea)
            linea.unidades = float(txt_unidades.text().replace(',', '.'))
            LineaFacturaRepository.save(linea)
            self.load_lineas_factura_en_tab_ventas()
            self.descontar()

        except Exception as e:
            print(f'Error al actualizar unidades en linea de factura: {e}')

    def actualizar_cmb_linea_factura(self, id_linea):
        """

        Evento asociado al escuchador vinculado al QComboBox de servicios en la línea de factura.

        :param id_linea: de factura
        """
        try:
            line = self.view_holder.get(id_linea)
            cmb_servicio: QComboBox = line[0]
            servicio: Servicio = cmb_servicio.currentData()
            linea: LineaFactura = LineaFacturaRepository.getById(id_linea)
            linea.servicio = servicio
            LineaFacturaRepository.save(linea)
            self.load_lineas_factura_en_tab_ventas()
            self.descontar()
        except Exception as e:
            print(f'Error al actualizar linea por cmb {e}')

    def generar_nueva_linea_venta(self):
        """

        Genera una nueva línea de factur vacía en memoria que permite ser editada y añadir nuevas líneas a la factura.

        """
        try:
            factura = FacturaRepository.getById(int(self.ui.txtNumFactura.text()))
            if not factura.emitida:
                line = self.cargaLineaVenta(len(factura.lineas_de_factura))

                # combobox
                cmb_concepto = line[0]
                cmb_concepto.currentIndexChanged.connect(
                    partial(self.actualizar_precio_nueva_linea_venta_por_cmb, line))

                # unidades
                txt_unidades = line[2]
                txt_unidades.editingFinished.connect(
                    partial(self.actualizar_precio_nueva_linea_venta_por_unidades, line))

                # eliminar
                btn_eliminar = line[4]
                btn_eliminar.setHidden(True)
                btn_eliminar.setEnabled(False)
            self.descontar()
        except Exception as e:
            print(f'Error al generar nueva linea de venta: {e}')

    def actualizar_precio_nueva_linea_venta_por_unidades(self, line):
        """

        Evento asociado al QLineEdit que actualiza el subtotal de la linea de venta indicada.

        :param line: linea de venta a actualizar

        """
        try:
            cmb_concepto: QComboBox = line[0]
            serv: Servicio = cmb_concepto.currentData()
            id_servicio = serv.codigo

            txt_unidades: QLineEdit = line[2]
            unidades = float(txt_unidades.text().replace(',', '.'))

            id_factura = int(self.ui.txtNumFactura.text())

            nuevaLinea = LineaFactura(servicio=ServicioRepository.getById(id_servicio))
            nuevaLinea.id_factura = id_factura
            nuevaLinea.unidades = unidades

            LineaFacturaRepository.save(nuevaLinea)

            self.load_lineas_factura_en_tab_ventas()
            self.generar_nueva_linea_venta()
        except Exception as e:
            print(f'Error actualizando nueva linea por unidades: {e}')

    def actualizar_precio_nueva_linea_venta_por_cmb(self, line):
        """

        Evento asociado al QComboBox que actualiza el subtotal de la linea de venta indicada.

        :param line: linea de venta a actualizar

        """
        try:
            cmb_concepto: QComboBox = line[0]
            serv: Servicio = cmb_concepto.currentData()
            txt_precio: QLineEdit = line[1]
            txt_precio.setText(serv.precio_unidad)
        except Exception as e:
            print(f'Error en actualizar_precio_nueva_linea_venta_por_cmb: {e}')

    def baja_factura(self):
        """

        Evento que permite dar de baja una factura

        """
        try:
            cliente: Cliente = ClienteRepository.getById(self.ui.txtDniCliFactura.text())
            factura_a_borrar: Factura = FacturaRepository.getById(int(self.ui.txtNumFactura.text()))

            cliente.facturas.remove(factura_a_borrar)
            FacturaRepository.remove(factura_a_borrar)
            ClienteRepository.save(cliente)

            self.ui.txtNumFactura.clear()
            self.ui.txtDniCliFactura.clear()
            self.ui.txtMatriculaFactura.clear()
            self.ui.txtFechaAltaFactura.clear()
            self.ui.txtBuscadorFactura.clear()

            self.load_table_facturas_data()

        except Exception as e:
            print(f'Error al dar de baja una factura: {e}')

    def alta_factura(self):
        """

        Evento que permite dar de alta una factura nueva

        """
        try:
            cliente = ClienteRepository.getById(self.ui.txtDniCliFactura.text())
            nueva_factura = Factura()
            nueva_factura.cliente = cliente
            nueva_factura.id_cliente = cliente.dni
            nueva_factura.matricula = self.ui.txtMatriculaFactura.text()
            nueva_factura.fecha = self.ui.txtFechaAltaFactura.text()

            cliente.addFactura(nueva_factura)
            ClienteRepository.save(cliente)

            nueva_factura = FacturaRepository.getLastInsert()
            self.ui.txtNumFactura.setText(str(nueva_factura.codigo_factura))
            self.load_table_facturas_data()

            self.ui.tab_facturas.selectRow(self.ui.tab_facturas.rowCount() - 1)


        except Exception as e:
            print(f'Error al dar de alta una factura nueva: {e}')

    def buscar_factura(self):
        """

        Evento asociado a la búsqueda de facturas desde el buscador de la tabla facturas.

        """
        try:
            arg = self.ui.txtBuscadorFactura.text()
            if re.match(r'^\d{8}[A-HJ-NP-TV-Z]$', arg):
                facturas = FacturaRepository.getByClienteId(arg)
                if facturas is not []:
                    for index, factura in enumerate(facturas):
                        self.ui.tab_facturas.setRowCount(index + 1)
                        self.ui.tab_facturas.setItem(index, 0, QTableWidgetItem(str(factura.codigo_factura)))
                        self.ui.tab_facturas.setItem(index, 1, QTableWidgetItem(factura.id_cliente))
                        self.ui.tab_facturas.setItem(index, 2, QTableWidgetItem(factura.matricula))
                else:
                    self.limpiar_tabla_facturas()

            elif arg.isnumeric():
                factura = FacturaRepository.getById(arg)
                if factura is not None:
                    self.ui.tab_facturas.setRowCount(1)
                    self.ui.tab_facturas.setItem(0, 0, QTableWidgetItem(str(factura.codigo_factura)))
                    self.ui.tab_facturas.setItem(0, 1, QTableWidgetItem(factura.id_cliente))
                    self.ui.tab_facturas.setItem(0, 2, QTableWidgetItem(factura.matricula))
                else:
                    self.limpiar_tabla_facturas()
            else:
                self.limpiar_tabla_facturas()

        except Exception as e:
            print(f'Error al buscar factura por argumento: {e}')

    def load_lineas_factura_en_tab_ventas(self):
        """

        Carga las líneas de una factura en la tbla de ventas para poder ser visualziadas por el usuario.

        """
        subtotal = 0
        iva = 21

        try:
            self.ui.txtBuscadorFactura.setText(str(self.ui.tab_facturas.selectedItems()[1].text()))
            codigo_factura = self.ui.tab_facturas.selectedItems()[0].text()
            factura = FacturaRepository.getById(codigo_factura)
            self.ui.txtDniCliFactura.setText(factura.id_cliente)
            self.ui.txtMatriculaFactura.setText(factura.matricula)
            self.ui.txtFechaAltaFactura.setText(factura.fecha)
            self.ui.txtNumFactura.setText(codigo_factura)

            self.ui.etDescuento.setText(str(FacturaRepository.getById(factura.codigo_factura).descuento))
            self.descontar()

            if factura.emitida:
                self.ui.btnEmitirFactura.setVisible(False)
                self.ui.tab_ventas.setEnabled(False)
                self.ui.lbl_factura_emitida.setVisible(True)
                self.ui.lbl_factura_emitida_desc.setVisible(True)

                self.ui.etDescuento.setEnabled(False)
                self.ui.btnAplicarDescuento.setEnabled(False)

            else:
                self.ui.btnEmitirFactura.setVisible(True)
                self.ui.tab_ventas.setEnabled(True)
                self.ui.lbl_factura_emitida.setVisible(False)
                self.ui.lbl_factura_emitida_desc.setVisible(False)
                self.ui.etDescuento.setEnabled(True)
                self.ui.btnAplicarDescuento.setEnabled(True)

            lineas = LineaFacturaRepository.getByFacturaId(int(codigo_factura))
            if len(lineas) == 0:
                self.limpiar_tabla_ventas()
                self.ui.tab_ventas.removeRow(0)
                self.view_holder.clear()
                self.ui.btnEmitirFactura.setEnabled(False)
                self.ui.tab_ventas.setVisible(True)

                self.ui.btnBajaFactura.setEnabled(False)
                self.ui.btnImprimirFactura.setEnabled(False)
            else:
                self.ui.tab_ventas.setVisible(True)
                self.view_holder.clear()
                for index, linea in enumerate(lineas):
                    self.view_holder[linea.id] = self.cargaLineaVenta(index, linea)
                    subtotal = subtotal + float(float(linea.precio) * (float(linea.unidades)))

                self.ui.txtSubtotal.setText(str('{:.2f}'.format(subtotal)))
                self.ui.txtIVA.setText(str(iva) + '%')
                self.ui.txtTotal.setText(str('{:.2f}'.format(subtotal + subtotal * iva / 100)))
                self.ui.txtBuscadorFactura.setText(str(factura.id_cliente))

                self.ui.btnEmitirFactura.setEnabled(True)

                self.generador_escuchadores_view_holder()

                self.generar_nueva_linea_venta()

                self.ui.btnBajaFactura.setEnabled(True)
                self.ui.btnImprimirFactura.setEnabled(True)


        except Exception as e:
            self.ui.tab_ventas.setVisible(False)
            self.limpiar_tabla_ventas()
            self.ui.btnEmitirFactura.setEnabled(False)

            self.ui.lbl_factura_emitida_desc.setVisible(False)
            self.ui.lbl_factura_emitida.setVisible(False)
            self.ui.btnEmitirFactura.setVisible(False)

            self.ui.btnBajaFactura.setEnabled(False)
            self.ui.btnImprimirFactura.setEnabled(False)

            self.ui.etDescuento.setEnabled(False)
            self.ui.btnAplicarDescuento.setEnabled(False)

            print(f'Error al cargar las lineas de factura: {e}')

    def eliminar_linea_factura(self, id_linea):
        """

        Evento asociado al botón de eliminar línea de factura.

        :param id_linea: id de asociación dinámica a través del view holder

        """
        LineaFacturaRepository.remove_by_id(id_linea)
        self.load_lineas_factura_en_tab_ventas()
        self.generar_nueva_linea_venta()

    def limpiar_tabla_facturas(self):
        """
        Limpia la tabla de facturas

        """
        self.ui.tab_facturas.clearContents()
        self.limpiar_tabla_ventas()

        nrow = self.ui.tab_facturas.rowCount()
        for i in range(0, nrow - 1):
            self.ui.tab_facturas.removeRow(i)

    def limpiar_tabla_ventas(self):
        """

        Limpia la tabla de ventas.

        """
        self.ui.tab_ventas.clearContents()
        self.ui.txtSubtotal.setText('')
        self.ui.txtIVA.setText('')
        self.ui.txtTotal.setText('')

        nrow = self.ui.tab_ventas.rowCount()
        for i in range(0, nrow):
            self.ui.tab_ventas.removeRow(i)

    def load_datos_cliente_en_factura(self):
        """

        Carga en la pestaña facturas los datos del cliente seleccionado en la pestaña clientes.

        """
        try:
            self.ui.txtNumFactura.clear()
            self.ui.txtBuscadorFactura.clear()
            self.ui.tab_facturas.clearSelection()
            self.ui.txtDniCliFactura.setText(self.ui.txtDniCli.text())
            self.ui.txtMatriculaFactura.setText(self.ui.txtMatricula.text())
            self.ui.txtFechaAltaFactura.setText(self.ui.txtFechaAltaCli.text())
        except Exception as e:
            print(f'Error al cargar datos de facturación: {e}')

    def cargaLineaVenta(self, index, linea: LineaFactura = None):
        """

        Crea y carga una nueva línea de venta para ser editada y permitir añadir nuevas lineas.

        :param index: de la línea
        :param linea: de venta
        :return: array de vistas de la linea
        """
        try:
            cmb_servicio = QtWidgets.QComboBox()
            txt_precio = QtWidgets.QLineEdit()
            txt_unidades = QtWidgets.QLineEdit()
            txt_subtotal = QtWidgets.QLineEdit()
            txt_eliminar = QtWidgets.QPushButton()
            txt_eliminar.setIcon(QIcon("img/exit.png"))

            cmb_servicio.setFixedSize(240, 20)

            txt_precio.setFixedSize(100, 20)
            txt_precio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            txt_precio.setReadOnly(True)

            txt_unidades.setFixedSize(100, 20)
            txt_unidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            txt_subtotal.setFixedSize(100, 20)
            txt_subtotal.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            txt_subtotal.setReadOnly(True)

            txt_eliminar.setFixedSize(20, 20)

            self.ui.tab_ventas.setRowCount(index + 1)
            self.ui.tab_ventas.setCellWidget(index, 0, cmb_servicio)
            self.ui.tab_ventas.setCellWidget(index, 1, txt_precio)
            self.ui.tab_ventas.setCellWidget(index, 2, txt_unidades)
            self.ui.tab_ventas.setCellWidget(index, 3, txt_subtotal)
            self.ui.tab_ventas.setCellWidget(index, 4, txt_eliminar)

            servicios = ServicioRepository.getAll()
            for s in servicios:
                cmb_servicio.addItem(str(s.concepto), s)
                txt_precio.setText(s.precio_unidad + '€')

            txt_precio.setText(cmb_servicio.currentData().precio_unidad)

            self.ui.tab_ventas.resizeColumnsToContents()
            self.ui.tab_ventas.resizeRowsToContents()

            if linea is not None:
                txt_precio.setText(str('{:.2f}'.format(linea.precio).replace('.', ',')))
                txt_unidades.setText(str(linea.unidades).replace('.', ','))
                txt_subtotal.setText(
                    str('{:.2f}'.format(float(linea.precio) * float(linea.unidades))).replace('.', ','))
                cmb_servicio.setCurrentText(linea.servicio.concepto)

            return cmb_servicio, txt_precio, txt_unidades, txt_subtotal, txt_eliminar
        except Exception as e:
            print(f'Error al cargar linea de venta: {e}')

    def load_table_facturas_data(self):
        """

        Carga las facturas de la base de datos en la tabla de facturas para poder ser visualizadas por el usuario.

        """
        try:
            for index, factura in enumerate(FacturaRepository.getAll()):
                self.ui.tab_facturas.setRowCount(index + 1)
                self.ui.tab_facturas.setItem(index, 0, QTableWidgetItem(str(factura.codigo_factura)))
                self.ui.tab_facturas.setItem(index, 1, QTableWidgetItem(factura.id_cliente))
                self.ui.tab_facturas.setItem(index, 2, QTableWidgetItem(factura.matricula))
        except Exception as e:
            print(f'Error al cargar las facturas en la tabla: {e}')

        self.ui.txtBuscadorFactura.clear()
        self.ui.tab_facturas.clearSelection()

    ##################################################################################################

    def loadTempService(self):
        """

        Carga servicios de manera temporal.

        """
        self.temp_serv = self.load_selected_service_data()

    def eneableButt(self):
        """

        Activa botones en lógica de inteacción con usuario.

        """
        self.ui.btnModifServicio.setEnabled(True)

    def load_date(self, qDate):
        """

        Carga fecha actual

        :param qDate: objeto de fecha
        """
        try:
            data = ("{0}/{1}/{2}".format(qDate.day(), qDate.month(), qDate.year()))
            self.ui.txtFechaAltaCli.setText(data)
            self.dlg_calendar.hide()
        except Exception as e:
            print(f'Error al cargar la fecha de alta: {e}')

    def eneableBtns(self):
        """

        Activa botones en función de interacción de usuario.

        """
        try:
            if not self.ui.tabClientes.selectedItems() or (
                    self.ui.txtMatricula.text() == '' or self.ui.txtDniCli.text() == ''):
                self.ui.btnEliminarCli.setEnabled(False)
                self.ui.btnModifCli.setEnabled(False)
                if self.modifing:
                    self.ui.btnModifCli.setEnabled(True)
            else:
                self.ui.btnEliminarCli.setEnabled(True)
                self.ui.btnModifCli.setEnabled(True)

                if self.modifing:
                    self.ui.btnModifCli.setEnabled(True)
                    self.ui.btnEliminarCli.setEnabled(False)
                    self.ui.btnGuardaCli.setEnabled(False)
                    self.ui.btnLimpiarCli.setEnabled(False)
                    self.ui.btnBuscarCli.setEnabled(False)
                else:
                    self.ui.btnEliminarCli.setEnabled(True)
                    self.ui.btnGuardaCli.setEnabled(True)
                    self.ui.btnLimpiarCli.setEnabled(True)
                    self.ui.btnBuscarCli.setEnabled(True)

        except Exception as e:
            print('Error al activar botones')

    def add_service(self):
        """

        Evento para añadir servicios al sistema.

        """
        try:
            concepto = self.ui.txtConceptoServicio.text()
            precio = self.ui.txtPrecioServicio.text()

            if len(concepto) == 0 or len(precio) == 0:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Deben cubrirse los campos obligatorios.')
                msg.exec()
            else:
                self.servicios_dao.create(Servicio(concepto=concepto, precio_unidad=precio))

                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Servicio añadido con éxito.')
                msg.exec()
        except Exception as e:
            print(f'Error al añadir un servicio: {e}')
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Error al añadido un servicio.')
            msg.exec()

    def update_service(self):
        """

        Evento para actualizar servicios al sistema.

        """
        try:
            service: Servicio = self.temp_serv
            if service:
                self.ui.btnModifServicio.setEnabled(True)
            else:
                self.ui.btnModifServicio.setEnabled(False)
            service.concepto = self.ui.txtConceptoServicio.text()
            service.precio_unidad = self.ui.txtPrecioServicio.text()
            service.stock = int(self.ui.txtStock.text())
            self.servicios_dao.update(service)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Servicio actualizado con éxito.')
            msg.exec()
        except Exception as e:
            print(f'Error al actualizar un servicio: {e}')
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Error al actualizar el servicio.')
            msg.exec()

    def load_table_style(self):
        """

        Carga estilo CSS de tabla de manera procedimental.

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

    def load_table_services_style(self):
        """

        Carga los estilos de la tabla servicio de manera procedimental.

        """
        try:
            # ajuste de tabla a marco
            header = self.ui.tabServicios.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            # aplicación de color a tabla
            self.ui.tabServicios.setStyleSheet(
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

    def load_table_facturas_style(self):
        """

        Carga los estilos de la tabla factura de manera procedimental.

        """
        try:
            # ajuste de tabla a marco
            header = self.ui.tab_facturas.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

            # aplicación de color a tabla
            self.ui.tab_facturas.setStyleSheet(
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

    def load_table_services_data(self):
        """

        Carga los datos de la tabla servicio de manera procedimental.

        """

        try:
            servicios = self.servicios_dao.read()
            servicios.pop(0)
            if len(servicios) == 0:
                self.ui.tabServicios.clearContents()
            else:
                for index, serv in enumerate(servicios):
                    self.ui.tabServicios.setRowCount(index + 1)
                    self.ui.tabServicios.setItem(index, 0, QTableWidgetItem(str(serv.codigo)))
                    self.ui.tabServicios.setItem(index, 1, QTableWidgetItem(str(serv.concepto).title()))
                    self.ui.tabServicios.setItem(index, 2, QTableWidgetItem(serv.precio_unidad))
                    self.ui.tabServicios.setItem(index, 3, QTableWidgetItem(str(serv.stock)))
        except Exception as e:
            print(f'Error al cargar los datos en la tabla: {e}')

    def delete_service(self):
        """

        Evento de borrado de servicios

        """
        try:
            service: Servicio = self.load_selected_service_data()
            self.servicios_dao.delete(service.codigo)
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Servicio eliminado con éxito.')
            msg.exec()
        except Exception as e:
            print(f'Error al borrar un servicio: {e}')
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Error al eliminar el servicio.')
            msg.exec()

    def load_selected_service_data(self):
        """

        Carga los datos seleccionados en la tabla servicio.

        """
        try:
            self.ui.txtConceptoServicio.setText("")
            self.ui.txtPrecioServicio.setText("")
            self.ui.txtStock.setText("")
            fila = self.ui.tabServicios.selectedItems()
            datos = [self.ui.txtConceptoServicio, self.ui.txtPrecioServicio, self.ui.txtStock]
            row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i + 1])
            return Servicio(codigo=row[0], concepto=row[1], precio_unidad=row[2], stock=row[3])
        except Exception as e:
            print(f'Error al cargar datos en la interfaz: {e}')

    def load_provincias(self):
        """

        Evento de carga de provincias en el QComboBox.

        """
        try:
            self.ui.cmbProCli.addItem('')
            provincias = self.provincias_dao.read()
            for p in provincias:
                self.ui.cmbProCli.addItem(p.nombre, p)
        except Exception as e:
            print(f'Error al cargar las provincias: {e}')

    def load_table_data(self):
        """

        Evento de carga de datos en la tabla de clientes.

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

        Evento de carga de provincias en QComboBox.

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

        Evento de carga de municipios en QComboBox

        """
        try:
            self.ui.cmbMuniCli.clear()
            cd = self.ui.cmbProCli.currentData()
            if cd is not None:
                for muni in cd.municipios:
                    self.ui.cmbMuniCli.addItem(muni.nombre, muni)
        except Exception as e:
            print(f'Error al cargar los municipios: {e}')

    def save_cliente(self):
        """

        Evento de guardado de cliente

        """
        try:
            dni = self.ui.txtDniCli.text()
            nombre = self.ui.txtNombreCli.text()
            alta = self.ui.txtFechaAltaCli.text()
            direccion = self.ui.txtDirCli.text()
            provincia = self.ui.cmbProCli.currentText()
            municipio = self.ui.cmbMuniCli.currentText()
            pago = ''
            if self.ui.chkTarjeta.isChecked():
                pago += 'tarjeta;'
            if self.ui.chkEfectivo.isChecked():
                pago += 'efectivo;'
            if self.ui.chkTransferencia.isChecked():
                pago += 'transferencia;'
            if dni == '' or nombre == '' or alta == '' or pago == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Deben cubrirse los campos obligatorios.')
                msg.exec()
                raise Exception('Deben cubrirse los campos obligatorios')
            elif not DniManager.validate_dni(dni):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('DNI inválido.')
                msg.exec()
                raise Exception('DNI inválido.')
            matricula = self.ui.txtMatricula.text()
            marca = self.ui.txtMarca.text()
            modelo = self.ui.txtModelo.text()
            if self.ui.rbtGasolina.isChecked():
                motor = 'Gasolina'
            elif self.ui.rbtDiesel.isChecked():
                motor = 'Diésel'
            elif self.ui.rbtHibrido.isChecked():
                motor = 'Híbrido'
            elif self.ui.rbtElectrico.isChecked():
                motor = 'Eléctrico'
            else:
                motor = 'Gasolina'
            if matricula == '' or motor == '' or marca == '' or modelo == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Deben cubrirse los campos obligatorios.')
                msg.exec()
                raise Exception('Deben cubrirse los campos obligatorios')
            cliente = Cliente(dni, nombre, alta, direccion, provincia, municipio, pago)
            coche = Coche(matricula, marca, modelo, motor, cliente)
            if self.coche_dao.exists(coche.matricula):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Ya existe un coche con esa matrícula.')
                msg.exec()
                raise Exception('Ya existe un coche con esa matrícula.')
            if not self.cliente_dao.exists(cliente):
                if self.cliente_dao.create(cliente):
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('Un nuevo cliente ha sido dado de alta.')
                    msg.exec()
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('Error al dar de alta a un nuevo cliente.')
                    msg.exec()
            else:
                self.cliente_dao.update(cliente)

            if self.coche_dao.create(coche):
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText(f'Un nuevo coche se ha dado de alta para {coche.propietario.nombre}.')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Error al dar de alta un coche.')
                msg.exec()
        except Exception as e:
            print(f'Error al cargar los datos: {e}')

    def delete_cliente(self):
        """

        Evento de borrado de cliente

        """
        try:
            dni = self.ui.txtDniCli.text()
            self.cliente_dao.delete_by_dni(dni)
            self.coche_dao.delete_by_client_dni(dni)
            self.load_table_data()
            self.dlg_historial.load_table_data()
        except Exception as e:
            print(f'Error al eliminar un cliente {e}')

    def create_backup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            copia = (str(fecha) + '_backup.zip')
            directorio, filename = self.dlg_open_file.getSaveFileName(None, 'Guardar copia', copia, '.zip')
            if self.dlg_open_file.accept and filename != '':
                fichzip = zipfile.ZipFile(copia, 'w')
                fichzip.write(ConnectionManager.filedb, os.path.basename(ConnectionManager.filedb),
                              zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Copia de seguridad creada.')
                msg.exec()
        except Exception as e:
            print('Error al crear backup.', e)
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Error al crear backup.')
            msg.exec()

    def restore_backup(self):
        """

        Evento de restauración de backups externos a la aplicación.

        """
        try:
            filename = self.dlg_open_file.getOpenFileName(None,
                                                          'Restaurar copia de seguridad',
                                                          '',
                                                          'All Files (*);;zip (*.zip)')
            if self.dlg_open_file.accept and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None, path='./db')
                bbdd.close()
            self.load_table_data()

            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Copia de seguridad restaurada')
            msg.exec()
        except Exception as e:
            print(f'Error al restaurar los datos: {e}')

    def load_selected_data(self):
        """

        Evento de carga de datos del cliente seleccionado e tabla clientes.

        :return: cliente seleccionado
        """
        try:
            self.clear_ui()
            fila = self.ui.tabClientes.selectedItems()
            datos = [self.ui.txtDniCli, self.ui.txtMatricula, self.ui.txtMarca, self.ui.txtModelo]
            row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            if row[4] == 'Diesel':
                self.ui.rbtDiesel.setChecked(True)
            elif row[4] == 'Gasolina':
                self.ui.rbtGasolina.setChecked(True)
            elif row[4] == 'Híbrido':
                self.ui.rbtHibrido.setChecked(True)
            elif row[4] == 'Eléctrico':
                self.ui.rbtElectrico.setChecked(True)
            cliente: Cliente = self.coche_dao.read(row[0])[0].propietario
            self.ui.txtNombreCli.setText(cliente.nombre)
            self.ui.txtFechaAltaCli.setText(cliente.alta)
            self.ui.txtDirCli.setText(cliente.direccion)
            self.ui.txtDniCli.setText(cliente.dni)
            self.ui.cmbProCli.setCurrentText(cliente.provincia)
            self.ui.cmbMuniCli.setCurrentText(cliente.municipio)

            tipo_pago = cliente.pago
            if 'efectivo' in tipo_pago:
                self.ui.chkEfectivo.setChecked(True)
            if 'transferencia' in tipo_pago:
                self.ui.chkTransferencia.setChecked(True)
            if 'tarjeta' in tipo_pago:
                self.ui.chkTarjeta.setChecked(True)

            self.dlg_del_client.load_client_data(cliente.dni, cliente.nombre)
            return cliente
        except Exception as e:
            print(f'Error al cargar datos en la interfaz: {e}')

    def clear_ui(self):
        """

        Evento de limpieza de interfaz

        """
        try:
            txt_ui = [
                self.ui.txtDniCli,
                self.ui.txtNombreCli,
                self.ui.txtDirCli,
                self.ui.txtFechaAltaCli,
                self.ui.txtMatricula,
                self.ui.txtMarca,
                self.ui.txtModelo
            ]
            btn_ui = [
                self.ui.chkTarjeta,
                self.ui.chkEfectivo,
                self.ui.chkTransferencia
            ]
            for d in txt_ui:
                d.setText("")
            for b in btn_ui:
                b.setChecked(False)
            self.ui.cmbProCli.setCurrentText('')
            self.ui.cmbMuniCli.setCurrentText('')

        except Exception as e:
            print(f'Error al limpiar la interfaz de datos: {e}')

    def text_lbl_to_mayus(self):
        """

        Evento de transformación de cadenas de texto

        """
        try:
            self.ui.txtNombreCli.setText(self.ui.txtNombreCli.text().title())
            self.ui.txtMarca.setText(self.ui.txtMarca.text().title())
            self.ui.txtModelo.setText(self.ui.txtModelo.text().title())
            self.ui.txtDirCli.setText(self.ui.txtDirCli.text().title())
            self.ui.txtMatricula.setText(self.ui.txtMatricula.text().upper())
            self.ui.txtPrecioServicio.setText(self.ui.txtPrecioServicio.text().title())
            self.ui.txtConceptoServicio.setText(self.ui.txtConceptoServicio.text().title())
        except Exception as error:
            print("Error al procesar las letras capitales", error)

    def dni_validator(self):
        """

        Evento validador de dni en base a las reglas estándar de formación de DNI español.

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

    def modify_data(self):
        """

        Evento de modificación segura de datos de clientes.

        """
        if self.modifing:
            self.modifing = False
            self.interface_status1 = self._end_modify()
            self.ui.btnModifCli.setStyleSheet('''
                            background-color: none
                        ''')
            if not self.interface_status1.__eq__(self.interface_status2):
                data = self.read_interface()
                cliente = Cliente(data.get('dni'),
                                  data.get('nombre'),
                                  data.get('fecha_alta'),
                                  data.get('direccion'),
                                  data.get('provincia'),
                                  data.get('municipio'),
                                  data.get('formas_pago'))
                coche = Coche(
                    data.get('matricula'),
                    data.get('marca'),
                    data.get('modelo'),
                    data.get('motor'),
                    cliente,
                )

                print(cliente.alta)
                ctrl1 = self.cliente_dao.update(cliente)
                ctrl2 = self.coche_dao.update(coche)
                if ctrl1 or ctrl2:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('Datos actualizados con éxito.')
                    msg.exec()
                    self.load_table_data()

        elif not self.modifing:
            self.modifing = True
            self.ui.btnModifCli.setStyleSheet('''
                background-color:#f0faaa
            ''')
            self.interface_status2 = self._start_modify()

    def _start_modify(self):
        color_amarillo = '#f0faaa'
        color_gris = '#B9B9B9'
        self.ui.txtDniCli.setReadOnly(True)
        self.ui.txtMatricula.setReadOnly(True)
        self.ui.txtDniCli.setStyleSheet("background-color:" + color_gris)
        self.ui.txtMatricula.setStyleSheet("background-color:" + color_gris)
        self.ui.txtNombreCli.setStyleSheet("background-color:" + color_amarillo)
        self.ui.txtMarca.setStyleSheet("background-color:" + color_amarillo)
        self.ui.txtModelo.setStyleSheet("background-color:" + color_amarillo)
        self.ui.txtFechaAltaCli.setStyleSheet("background-color:" + color_amarillo)
        self.ui.txtDirCli.setStyleSheet("background-color:" + color_amarillo)
        self.ui.tabClientes.setEnabled(False)
        return self.read_interface()

    def _end_modify(self):
        self.ui.txtDniCli.setReadOnly(False)
        self.ui.txtMatricula.setReadOnly(False)
        self.ui.txtDniCli.setStyleSheet("background-color: none")
        self.ui.txtMatricula.setStyleSheet("background-color: none")
        self.ui.txtNombreCli.setStyleSheet("background-color: none")
        self.ui.txtMarca.setStyleSheet("background-color: none")
        self.ui.txtModelo.setStyleSheet("background-color: none")
        self.ui.txtFechaAltaCli.setStyleSheet("background-color: none")
        self.ui.txtDirCli.setStyleSheet("background-color: none")
        self.ui.tabClientes.setEnabled(True)
        return self.read_interface()

    def read_interface(self):
        """

        Evento de captura de datos de interfaz gráfica de usuario.

        """
        try:
            formas_pago = ''
            if self.ui.rbtDiesel.isChecked():
                motor = 'Diesel'
            elif self.ui.rbtGasolina.isChecked():
                motor = 'Gasolina'
            elif self.ui.rbtHibrido.isChecked():
                motor = 'Híbrido'
            elif self.ui.rbtElectrico.isChecked():
                motor = 'Eléctrico'
            else:
                motor = ''
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

                'matricula': self.ui.txtMatricula.text(),
                'marca': self.ui.txtMarca.text(),
                'modelo': self.ui.txtModelo.text(),

                'formas_pago': formas_pago,
                'motor': motor}
        except Exception as e:
            print(f'Error al leer la interface: {e}')
