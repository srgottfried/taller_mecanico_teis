# Form implementation generated from reading ui file 'C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views/dlgEligeCampos.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgEligeCampos(object):
    def setupUi(self, dlgEligeCampos):
        dlgEligeCampos.setObjectName("dlgEligeCampos")
        dlgEligeCampos.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        dlgEligeCampos.resize(313, 222)
        self.verticalLayoutWidget = QtWidgets.QWidget(dlgEligeCampos)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 70, 96, 59))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.chkClientes = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.chkClientes.setStyleSheet("font: 500 10pt \"MS Shell Dlg 2\";")
        self.chkClientes.setChecked(True)
        self.chkClientes.setObjectName("chkClientes")
        self.verticalLayout.addWidget(self.chkClientes)
        self.chkCoches = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.chkCoches.setStyleSheet("font: 500 10pt \"MS Shell Dlg 2\";")
        self.chkCoches.setChecked(True)
        self.chkCoches.setObjectName("chkCoches")
        self.verticalLayout.addWidget(self.chkCoches)
        self.btnAceptar = QtWidgets.QPushButton(dlgEligeCampos)
        self.btnAceptar.setGeometry(QtCore.QRect(80, 170, 141, 25))
        self.btnAceptar.setMinimumSize(QtCore.QSize(75, 25))
        self.btnAceptar.setStyleSheet("font: 500 10pt \"MS Shell Dlg 2\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views\\../img/verified.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnAceptar.setIcon(icon)
        self.btnAceptar.setObjectName("btnAceptar")
        self.label = QtWidgets.QLabel(dlgEligeCampos)
        self.label.setGeometry(QtCore.QRect(20, 10, 281, 31))
        self.label.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlgEligeCampos)
        self.label_2.setGeometry(QtCore.QRect(70, 60, 71, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/a21manuellg/Desktop/2DAM/DI/workspace/landingomez/views\\../img/export.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(dlgEligeCampos)
        QtCore.QMetaObject.connectSlotsByName(dlgEligeCampos)

    def retranslateUi(self, dlgEligeCampos):
        _translate = QtCore.QCoreApplication.translate
        dlgEligeCampos.setWindowTitle(_translate("dlgEligeCampos", "Exportando hoja de datos"))
        self.chkClientes.setText(_translate("dlgEligeCampos", "Clientes"))
        self.chkCoches.setText(_translate("dlgEligeCampos", "Coches"))
        self.btnAceptar.setText(_translate("dlgEligeCampos", "Aceptar"))
        self.label.setText(_translate("dlgEligeCampos", "Seleccione las hojas de exportación:"))
