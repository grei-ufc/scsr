# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogLine.ui'
#
# Created: Mon Feb  9 00:19:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui
import sys

class LineDialog(QtWidgets.QWidget):

    def __init__(self):
        super(LineDialog, self).__init__()
        self.dialog = QtWidgets.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(428, 180)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 130, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 401, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.comprimentoMLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.comprimentoMLabel.setObjectName("comprimentoMLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.comprimentoMLabel)
        self.comprimentoMLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.comprimentoMLineEdit.setObjectName("comprimentoMLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comprimentoMLineEdit)
        self.impedNciaPorComprimentoLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.impedNciaPorComprimentoLabel.setObjectName("impedNciaPorComprimentoLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.impedNciaPorComprimentoLabel)
        self.impedNciaPorComprimentoLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.impedNciaPorComprimentoLineEdit.setObjectName("impedNciaPorComprimentoLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.impedNciaPorComprimentoLineEdit)
        self.limiteDeOperaOALabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.limiteDeOperaOALabel.setObjectName("limiteDeOperaOALabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.limiteDeOperaOALabel)
        self.limiteDeOperaOALineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.limiteDeOperaOALineEdit.setObjectName("limiteDeOperaOALineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.limiteDeOperaOALineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Alimentador - Propriedades", None, int=-1))
        self.comprimentoMLabel.setText(QtWidgets.QApplication.translate("Dialog", "Comprimento (m):", None, int=-1))
        self.impedNciaPorComprimentoLabel.setText(QtWidgets.QApplication.translate("Dialog", "Impedância por Comprimento (ohms/m)", None, int=-1))
        self.limiteDeOperaOALabel.setText(QtWidgets.QApplication.translate("Dialog", "Limite de Operação (A)", None, int=-1))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialogLinha = LineDialog()
    sys.exit(app.exec_())