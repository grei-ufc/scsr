# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aviso_conexao.ui'
#
# Created: Sun Mar 15 15:28:01 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import sys

class AvisoConexaoDialog(QtWidgets.QWidget):

    def __init__(self):
        super(AvisoConexaoDialog, self).__init__()
        self.dialog = QtWidgets.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(332, 86)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 50, 81, 27))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 311, 21))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Erro", None, int=-1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, int=-1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Você deve excluir as outras conexões primeiro!", None, int=-1))

