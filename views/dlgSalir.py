# Form implementation generated from reading ui file 'C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views/dlgSalir.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgSalir(object):
    def setupUi(self, dlgSalir):
        dlgSalir.setObjectName("dlgSalir")
        dlgSalir.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        dlgSalir.resize(300, 200)
        dlgSalir.setMinimumSize(QtCore.QSize(300, 200))
        dlgSalir.setMaximumSize(QtCore.QSize(300, 200))
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgSalir)
        self.buttonBox.setGeometry(QtCore.QRect(50, 150, 200, 30))
        self.buttonBox.setMinimumSize(QtCore.QSize(200, 30))
        self.buttonBox.setMaximumSize(QtCore.QSize(200, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.imgAviso = QtWidgets.QLabel(dlgSalir)
        self.imgAviso.setGeometry(QtCore.QRect(110, 30, 81, 61))
        self.imgAviso.setText("")
        self.imgAviso.setPixmap(QtGui.QPixmap("C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views\\../img/warning.png"))
        self.imgAviso.setScaledContents(True)
        self.imgAviso.setObjectName("imgAviso")
        self.lblSalir = QtWidgets.QLabel(dlgSalir)
        self.lblSalir.setGeometry(QtCore.QRect(80, 110, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblSalir.setFont(font)
        self.lblSalir.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblSalir.setObjectName("lblSalir")

        self.retranslateUi(dlgSalir)
        self.buttonBox.accepted.connect(dlgSalir.accept) # type: ignore
        self.buttonBox.rejected.connect(dlgSalir.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dlgSalir)

    def retranslateUi(self, dlgSalir):
        _translate = QtCore.QCoreApplication.translate
        dlgSalir.setWindowTitle(_translate("dlgSalir", "Salir"))
        self.lblSalir.setText(_translate("dlgSalir", "¿Desea salir?"))