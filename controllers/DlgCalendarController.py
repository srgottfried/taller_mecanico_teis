from datetime import datetime
from PyQt6.QtWidgets import QDialog
from PyQt6 import QtCore

import views


class DlgCalendarController(QDialog):
    def __init__(self):
        super(DlgCalendarController, self).__init__()

        # Variable de acceso a widgets y carga de vista en controlador
        self.ui = views.Ui_dlgCalendar()
        self.ui.setupUi(self)

        # Cargamos el día actual en el calendario
        dia = datetime.now().day
        mes = datetime.now().month
        anno = datetime.now().year
        self.ui.Calendar.setSelectedDate(QtCore.QDate(anno, mes, dia))
