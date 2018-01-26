# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogBarra.ui'
#
# Created: Sun Mar  1 19:05:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import sys
class BarraDialog(QtWidgets.QWidget):

    def __init__(self, item):
        super(BarraDialog, self).__init__()
        self.dialog = QtWidgets.QDialog(None)
        self.item = item
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Propriedades):
        Propriedades.setObjectName("Propriedades")
        Propriedades.resize(380, 271)
        #Define o tamanho da caixa dialogo
        self.buttonBox = QtWidgets.QDialogButtonBox(Propriedades)
        self.buttonBox.setGeometry(QtCore.QRect(0, 231, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Propriedades)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 231))
        #Define a localização do layout das propriedades (coordenada x do ponto, coordenada y do ponto, dimensão em x, dimensão em y)
        
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        #definição da propriedade NOME
        self.nomeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nomeLabel.setObjectName("nomeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nomeLabel)
        self.nomeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nomeLineEdit.setObjectName("nomeLineEdit")
        self.nomeLineEdit.setPlaceholderText(str(self.item.barra.nome))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nomeLineEdit)
        self.fasesLabel = QtWidgets.QLabel(self.formLayoutWidget)

        #definição da propriedade FASES
        self.fasesLabel.setObjectName("fasesLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fasesLabel)
        self.fasesLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.fasesLineEdit.setObjectName("fasesLineEdit")
        self.fasesLineEdit.setPlaceholderText(str(self.item.barra.phases))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fasesLineEdit)

        #definição da propriedade IMPEDANCIA SEQUENCIA POSITIVA
        self.r_posLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.r_posLabel.setObjectName("r_posLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.r_posLabel)
        self.r_posLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.r_posLineEdit.setObjectName("r_posLineEdit")
        self.r_posLineEdit.setPlaceholderText(str(self.item.barra.r_pos))
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.r_posLineEdit)

        self.i_posLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.i_posLabel.setObjectName("i_posLabel")
        self.i_posLabel.setAlignment(QtCore.Qt.AlignRight)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.i_posLabel)
        self.i_posLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.i_posLineEdit.setObjectName("i_posLineEdit")
        self.i_posLineEdit.setPlaceholderText(str(self.item.barra.i_pos))
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.i_posLineEdit)

        #definição da propriedade IMPEDANCIA SEQUENCIA ZERO
        self.r_zeroLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.r_zeroLabel.setObjectName("r_zeroLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.r_zeroLabel)
        self.r_zeroLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.r_zeroLineEdit.setObjectName("r_zeroLineEdit")
        self.r_zeroLineEdit.setPlaceholderText(str(self.item.barra.r_zero))
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.r_zeroLineEdit)

        self.i_zeroLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.i_zeroLabel.setObjectName("i_zeroLabel")
        self.i_zeroLabel.setAlignment(QtCore.Qt.AlignRight)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.i_zeroLabel)
        self.i_zeroLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.i_zeroLineEdit.setObjectName("i_zeroLineEdit")
        self.i_zeroLineEdit.setPlaceholderText(str(self.item.barra.i_zero))
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.i_zeroLineEdit)

        self.retranslateUi(Propriedades)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Propriedades.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Propriedades.reject)
        QtCore.QMetaObject.connectSlotsByName(Propriedades)

    def retranslateUi(self, Propriedades):
        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Propriedades.setWindowTitle(QtWidgets.QApplication.translate("Propriedades", "Barra - Propriedades", None, int=-1))
        self.nomeLabel.setText(QtWidgets.QApplication.translate("Propriedades", "Nome:", None, int=-1))
        self.fasesLabel.setText(QtWidgets.QApplication.translate("Propriedades", "Fases:", None, int=-1))
        self.r_posLabel.setText(QtWidgets.QApplication.translate("Dialog", "Impedância (Sequência Positiva):", None, int=-1))
        self.i_posLabel.setText(QtWidgets.QApplication.translate("Dialog", "+", None, int=-1))
        self.r_zeroLabel.setText(QtWidgets.QApplication.translate("Dialog", "Impedância (Sequência Zero):", None, int=-1))
        self.i_zeroLabel.setText(QtWidgets.QApplication.translate("Dialog", "+", None, int=-1))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    BarraDialog = BarraDialog()
    sys.exit(app.exec_())
