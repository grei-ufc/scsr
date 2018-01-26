# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'avisoReligador.ui'
#
# Created: Mon Apr 27 17:57:38 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import sys

class AvisoReligador(QtWidgets.QWidget):

    def __init__(self, estado, nome):
        super(AvisoReligador, self).__init__()
        self.estado = estado
        self.nome = nome
        self.dialog = QtWidgets.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 120)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(120, 70, 176, 27))
        self.buttonBox.addButton(QtWidgets.QPushButton("Sim"), QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QtWidgets.QPushButton(QtWidgets.QApplication.translate("Dialog", "Não", None, int=-1)), QtWidgets.QDialogButtonBox.RejectRole)
        #self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 420, 41))
        self.label.setObjectName("label")
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "AVISO!", None, int=-1))
        if self.estado == 0:
            self.label.setText(QtWidgets.QApplication.translate("Dialog", "Você tem certeza de que quer ABRIR o Religador " + str(self.nome) + "?", None, int=-1))
        else:
            self.label.setText(QtWidgets.QApplication.translate("Dialog", "Você tem certeza de que quer FECHAR o Religador "  + str(self.nome) + "?", None, int=-1))
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ReligadorAviso = AvisoReligador()
    sys.exit(app.exec_())
