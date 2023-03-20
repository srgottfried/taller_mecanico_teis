import os

from datetime import datetime
from reportlab.pdfgen import canvas

from daos import ClienteQtDao, CocheQtDao
from models import Cliente, Factura, Servicio
from repositories import ClienteRepository, FacturaRepository, ServicioRepository


class Informe:
    """

    Clase para la gestión de informes

    """

    def __init__(self):
        self.report = canvas.Canvas('informes/{}')
        self.file_name = None
        self.titulo = None
        self.path = '.\\informes'
        self.logo = '.\\img\\logo.jpg'
        self.cif = 'CIF: A12345678'
        self.direccion1 = 'Avda. Galicia -101'
        self.direccion2 = 'Vigo - 36216 - España'
        self.tlf = 'Teléfono: 611 644 655'
        self.email = 'email: talleres@teis.com'

    def list_clientes(self):
        self.titulo = 'LISTADO CLIENTES'
        self.file_name = 'listadoClientes.pdf'
        self.report = canvas.Canvas('informes/{}'.format(self.file_name))
        try:
            self.page_cliente()
            self.report.save()
            os.startfile('%s\%s' % (self.path, self.file_name))
        except Exception as e:
            print(f'Error al listar informe de cliente: {e}')

    def list_servicios(self):
        self.titulo = 'LISTADO SERVICIOS'
        self.file_name = 'listadoServicios.pdf'
        self.report = canvas.Canvas('informes/{}'.format(self.file_name))
        try:
            self.page_servicios()
            self.report.save()
            os.startfile('%s\%s' % (self.path, self.file_name))
        except Exception as e:
            print(f'Error al listar informe de servicios: {e}')

    def list_autos(self):
        self.titulo = 'LISTADO COCHES'
        self.file_name = 'listadoCoches.pdf'
        self.report = canvas.Canvas('informes/{}'.format(self.file_name))
        try:
            self.page_coches()
            self.report.save()
            os.startfile('%s\%s' % (self.path, self.file_name))
        except Exception as e:
            print(f'Error al listar informe de cliente: {e}')

    def list_facturas(self, view_factura):
        id_factura = view_factura.text()
        factura = FacturaRepository.getById(id_factura)

        self.titulo = 'Factura'
        self.file_name = 'factura.pdf'
        self.report = canvas.Canvas('informes/{}'.format(self.file_name))
        try:
            self.page_factura(factura=factura)
            self.report.save()
            os.startfile('%s\%s' % (self.path, self.file_name))
        except Exception as e:
            print(f'Error al listar informe de facturas: {e}')

    def page_coches(self):
        # HEADER -----------------
        self.cabecera_informe()
        # BODY -------------------
        self.body_informe_coche()
        # FOOTER -----------------
        self.pie_informe()

    def page_cliente(self):
        # HEADER -----------------
        self.cabecera_informe()
        # BODY -------------------
        self.body_informe_cliente()
        # FOOTER -----------------
        self.pie_informe()

    def page_servicios(self):
        # HEADER -----------------
        self.cabecera_informe()
        # BODY -------------------
        self.body_informe_servicio()
        # FOOTER -----------------
        self.pie_informe()

    def page_factura(self, factura):
        # HEADER -----------------
        self.cabecera_informe()
        # BODY -------------------
        self.body_informe_factura(factura=factura)
        # FOOTER -----------------
        self.pie_informe()


    def body_informe_factura(self, factura: Factura):
        try:

            total = 0
            numero_factura = 'Nº Factura: $'
            fecha_factura = 'Fecha: $'

            self.report.setFont('Helvetica-Bold', size=9)
            self.report.drawString(60, 670, 'DATOS CLIENTE:')
            self.report.drawString(400, 650, numero_factura.replace('$', str(factura.codigo_factura)))
            self.report.drawString(400, 635, fecha_factura.replace('$', str(factura.fecha)))
            self.report.setFont('Helvetica', size=9)


            dni_cif = 'DNI/CIF: $'
            nombre = 'Nombre: $'
            direccion = 'Dirección: $'
            provincia = 'Provincia: $'
            municipio = 'Municipio: $'

            cliente = ClienteRepository.getById(factura.id_cliente)

            self.report.drawString(60, 650, dni_cif.replace('$', cliente.dni))
            self.report.drawString(60, 635, nombre.replace('$', cliente.nombre))
            self.report.drawString(60, 620, direccion.replace('$', cliente.direccion))
            self.report.drawString(60, 605, provincia.replace('$', cliente.provincia))
            self.report.drawString(60, 590, municipio.replace('$', cliente.municipio))

            self.report.line(50, 580, 525, 580)
            self.report.line(50, 560, 525, 560)

            self.report.drawString(60, 565, 'ID')
            self.report.drawString(120, 565, 'Servicio')
            self.report.drawString(270, 565, 'Precio/Unidad')
            self.report.drawString(370, 565, 'Unidades')
            self.report.drawString(460, 565, 'Subtotal')

            i = 0
            k = 545
            for linea in factura.lineas_de_factura:
                j = k - 30 * i
                self.report.setFont('Helvetica', size=9)
                self.report.drawRightString(70, j, str(linea.servicio.codigo))
                self.report.drawString(120, j, str(linea.servicio.concepto))
                self.report.drawRightString(310, j, '{:.2f}'.format(linea.precio) + '€')
                self.report.drawString(380, j, str(linea.unidades))
                self.report.drawRightString(500, j, '{:.2f}'.format(linea.calcular_subtotal()).replace('.',',') + '€')
                total = total + linea.calcular_subtotal()
                i = i + 1

                if j <= 80:
                    self.pie_informe()
                    self.report.showPage()
                    i = 0
                    k = 740

                    self.report.line(50, 780, 525, 780)
                    self.report.setFont('Helvetica', size=9)
                    self.report.drawString(60, 765, 'ID')
                    self.report.drawString(120, 765, 'Servicio')
                    self.report.drawString(270, 765, 'Precio/Unidad')
                    self.report.drawString(370, 765, 'Unidades')
                    self.report.drawString(460, 765, 'Subtotal')
                    self.report.line(50, 760, 525, 760)

            total = total * 1.21


            if factura.descuento == 0:
                self.report.setFont('Helvetica-Bold', size=10)
                self.report.line(350, 145, 540, 145)
                self.report.drawRightString(420, 130, ' IVA: ')
                self.report.drawRightString(530, 130, str(round(21, 2)).replace('.', ',') + ' %')
                self.report.drawRightString(420, 110, ' TOTAL: ')
                self.report.drawRightString(530, 110, str(round(total, 2)).replace('.', ',') + ' €')
                self.report.line(350, 100, 540, 100)

            else:

                self.report.setFont('Helvetica-Bold', size=10)
                self.report.line(350, 180, 540, 180)
                self.report.drawRightString(420, 160, ' DESCUENTO: ')

                self.report.drawRightString(530, 160, '- ' + str(round(total *  factura.descuento/100, 2)).replace('.', ',') + ' €')
                self.report.drawRightString(420, 130, ' IVA: ')
                self.report.drawRightString(530, 130, str(round(21, 2)).replace('.', ',') + ' %')
                self.report.drawRightString(420, 110, ' TOTAL: ')
                self.report.drawRightString(530, 110, str(round(total, 2)).replace('.', ',') + ' €')
                self.report.line(350, 100, 540, 100)

        except Exception as e:
            print(f'Error en el body_informe_factura: {e}')

    def body_informe_cliente(self):
        items = ['DNI', 'NOMBRE', 'Dirección', 'Provincia', 'Municipio']
        self.report.setFont('Helvetica', size=10)
        self.report.drawString(60, 670, str(items[0]))
        self.report.drawString(120, 670, str(items[1]))
        self.report.drawString(210, 670, str(items[2]))
        self.report.drawString(320, 670, str(items[3]))
        self.report.drawString(400, 670, str(items[4]))
        self.report.line(50, 665, 525, 665)

        clientes = ClienteQtDao().readAll()
        i = 0
        k = 650

        for c in clientes:
            j = k - 30 * i
            self.report.setFont('Helvetica', size=9)
            self.report.drawString(60, j, self.hide_dni(c.dni))
            self.report.drawString(120, j, c.nombre)
            self.report.drawString(210, j, c.direccion)
            self.report.drawString(320, j, c.provincia)
            self.report.drawString(400, j, c.municipio)

            i = i + 1

            if j <= 100:
                self.pie_informe()
                self.report.showPage()
                i = 0
                k = 740

    def body_informe_coche(self):
        items = ['Matrícula', 'DNI', 'Marca', 'Modelo', 'Motor']
        self.report.setFont('Helvetica', size=10)
        self.report.drawString(60, 670, str(items[0]))
        self.report.drawString(120, 670, str(items[1]))
        self.report.drawString(210, 670, str(items[2]))
        self.report.drawString(300, 670, str(items[3]))
        self.report.drawString(460, 670, str(items[4]))
        self.report.line(50, 665, 525, 665)

        coches = CocheQtDao().read_altas_all()

        i = 0
        k = 650

        for c in coches:
            j = k - 30 * i
            self.report.setFont('Helvetica', size=9)
            self.report.drawString(60, j, c.matricula)
            self.report.drawString(120, j, self.hide_dni(c.propietario.dni))
            self.report.drawString(210, j, c.marca)
            self.report.drawString(300, j, c.modelo)
            self.report.drawString(460, j, c.motor)

            i = i + 1

            if j <= 100:
                self.pie_informe()
                self.report.showPage()
                i = 0
                k = 740


    def body_informe_servicio(self):
        items = ['CÓDIGO', 'CONCEPTO', 'STOCK', 'PRECIO/UNIDAD']
        self.report.setFont('Helvetica', size=10)
        self.report.drawString(60, 670, str(items[0]))
        self.report.drawString(120, 670, str(items[1]))
        self.report.drawString(320, 670, str(items[2]))
        self.report.drawString(410, 670, str(items[3]))
        self.report.line(50, 665, 525, 665)

        servicios = ServicioRepository.getAll()
        self.report.setFont('Helvetica', size=8)
        servicios.pop(0)

        i = 0
        k = 650

        for linea in servicios:
            j = k - 30 * i
            self.report.setFont('Helvetica', size=9)
            self.report.drawRightString(70, j, str(linea.codigo))
            self.report.drawString(120, j, str(linea.concepto))
            self.report.drawString(330, j, str(linea.stock))
            self.report.drawRightString(480, j, linea.precio_unidad + '€')

            i = i + 1

            if j <= 100:
                self.pie_informe()
                self.report.showPage()
                i = 0
                k = 740


    def pie_informe(self):
        try:
            self.report.line(50, 50, 525, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            self.report.setFont('Helvetica-Oblique', size=7)
            self.report.drawString(50, 40, str(fecha))
            self.report.drawString(250, 40, str(self.titulo))
            self.report.drawString(485, 40, 'Página {}'.format(self.report.getPageNumber()))
        except Exception as e:
            print(f'Error al construir el pie de informe: {e}')

    def cabecera_informe(self):
        try:
            self.report.line(50, 685, 525, 685)
            self.report.setFont('Helvetica-Bold', size=14)
            self.report.line(50, 790, 525, 790)
            self.report.drawString(55, 775, 'Taller Mecánico Teis')
            self.report.drawString(230, 695, self.titulo)
            self.report.drawImage(self.logo, 430, 695, width=100, height=80)
            self.report.setFont('Helvetica', size=10)
            self.report.drawString(60, 755, self.cif)
            self.report.drawString(60, 740, self.direccion1)
            self.report.drawString(60, 725, self.direccion2)
            self.report.drawString(60, 710, self.tlf)
            self.report.drawString(60, 695, self.email)
        except Exception as e:
            print(f'Error al construir la cabecera de informe: {e}')

    def hide_dni(self, dni):
        return f'*****{dni[5:8]}*'

    def generar_total(self):
        try:
            pass
        except Exception as e:
            print('Error al generar total en factura: ', e)
