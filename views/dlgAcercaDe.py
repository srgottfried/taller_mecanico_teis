# Form implementation generated from reading ui file 'C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views/dlgAcercaDe.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgAcercaDe(object):
    def setupUi(self, dlgAcercaDe):
        dlgAcercaDe.setObjectName("dlgAcercaDe")
        dlgAcercaDe.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        dlgAcercaDe.resize(456, 459)
        dlgAcercaDe.setMinimumSize(QtCore.QSize(300, 200))
        self.imgAviso = QtWidgets.QLabel(dlgAcercaDe)
        self.imgAviso.setGeometry(QtCore.QRect(140, 50, 171, 141))
        self.imgAviso.setText("")
        self.imgAviso.setPixmap(QtGui.QPixmap("C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views\\../img/logo.jpg"))
        self.imgAviso.setScaledContents(True)
        self.imgAviso.setObjectName("imgAviso")
        self.lblSalir = QtWidgets.QLabel(dlgAcercaDe)
        self.lblSalir.setGeometry(QtCore.QRect(110, 190, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblSalir.setFont(font)
        self.lblSalir.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblSalir.setObjectName("lblSalir")
        self.btnVolver = QtWidgets.QPushButton(dlgAcercaDe)
        self.btnVolver.setGeometry(QtCore.QRect(170, 390, 93, 28))
        self.btnVolver.setObjectName("btnVolver")
        self.label = QtWidgets.QLabel(dlgAcercaDe)
        self.label.setGeometry(QtCore.QRect(180, 260, 121, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlgAcercaDe)
        self.label_2.setGeometry(QtCore.QRect(100, 290, 301, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dlgAcercaDe)
        self.label_3.setGeometry(QtCore.QRect(120, 350, 261, 21))
        self.label_3.setStyleSheet("color:gray")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(dlgAcercaDe)
        QtCore.QMetaObject.connectSlotsByName(dlgAcercaDe)

    def retranslateUi(self, dlgAcercaDe):
        _translate = QtCore.QCoreApplication.translate
        dlgAcercaDe.setWindowTitle(_translate("dlgAcercaDe", "Salir"))
        self.lblSalir.setText(_translate("dlgAcercaDe", "TallerManager"))
        self.btnVolver.setText(_translate("dlgAcercaDe", "Volver"))
        self.label.setText(_translate("dlgAcercaDe", "Version 0.0.1"))
        self.label_2.setText(_translate("dlgAcercaDe", "TallerManage for Desktop Version 2023-03-08"))
        self.label_3.setText(_translate("dlgAcercaDe", "Copiright (c) 2023 TallerManager"))
