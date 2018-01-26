# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogConductor.ui'
#
# Created: Tue Mar 17 13:53:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui,QtWidgets  
import sys

class ConductorDialog(QtWidgets.QWidget):

    def __init__(self, item):
        super(ConductorDialog, self).__init__()
        self.dialog = QtWidgets.QDialog(self)
        self.item = item
        self.scene = self.item.scene()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 210)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 170, 341, 32))

        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 150))

        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.comprimentoLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.comprimentoLabel.setObjectName("comprimentoLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.comprimentoLabel)
        self.comprimentoLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.comprimentoLineEdit.setObjectName("comprimentoLineEdit")
        self.comprimentoLineEdit.setPlaceholderText(str(self.item.linha.comprimento))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comprimentoLineEdit)

        self.resistenciaLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.resistenciaLabel.setObjectName("resistenciaLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.resistenciaLabel)
        self.resistenciaLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.resistenciaLineEdit.setObjectName("resistenciaLineEdit")
        self.resistenciaLineEdit.setPlaceholderText(str(self.item.linha.resistencia))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.resistenciaLineEdit)

        self.resistenciaZeroLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.resistenciaZeroLabel.setObjectName("resistenciaZeroLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.resistenciaZeroLabel)
        self.resistenciaZeroLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.resistenciaZeroLineEdit.setObjectName("resistenciaZeroLineEdit")
        self.resistenciaZeroLineEdit.setPlaceholderText(str(self.item.linha.resistencia_zero))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.resistenciaZeroLineEdit)

        self.reatanciaLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.reatanciaLabel.setObjectName("reatanciaLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.reatanciaLabel)
        self.reatanciaLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.reatanciaLineEdit.setObjectName("reatanciaLineEdit")
        self.reatanciaLineEdit.setPlaceholderText(str(self.item.linha.reatancia))
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.reatanciaLineEdit)

        self.reatanciaZeroLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.reatanciaZeroLabel.setObjectName("reatanciaZeroLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.reatanciaZeroLabel)
        self.reatanciaZeroLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.reatanciaZeroLineEdit.setObjectName("reatanciaZeroLineEdit")
        self.reatanciaZeroLineEdit.setPlaceholderText(str(self.item.linha.reatancia_zero))
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.reatanciaZeroLineEdit)

        self.ampacidadeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.ampacidadeLabel.setObjectName("ampacidadeLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.ampacidadeLabel)
        self.ampacidadeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ampacidadeLineEdit.setObjectName("ampacidadeLineEdit")
        self.ampacidadeLineEdit.setPlaceholderText(str(self.item.linha.ampacidade))
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ampacidadeLineEdit)

        self.condutorLabel=QtWidgets.QLabel(self.formLayoutWidget)
        self.condutorLabel.setObjectName("condutorLabel")
        self.formLayout.setWidget(6,QtWidgets.QFormLayout.LabelRole,self.condutorLabel)
        self.condutorLineEdit=QtWidgets.QComboBox(self.formLayoutWidget)
        self.condutorLineEdit.setObjectName("condutorLineEdit")
        self.condutorLineEdit.insertItem(0,"Custom")
        self.condutorLineEdit.addItems(list(self.scene.dic_cab.keys()))
        self.condutorLineEdit.setCurrentIndex(self.condutorLineEdit.findText(self.item.text_config))
        self.condutorLineEdit.currentIndexChanged.connect(self._new_index)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.condutorLineEdit)




        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def _new_index(self):
        if self.condutorLineEdit.findText(self.condutorLineEdit.currentText())!=0:
            self.ampacidadeLineEdit.setText(str(self.scene.dic_cab[self.condutorLineEdit.currentText()]['ampacidade']))
            self.resistenciaLineEdit.setText(str(self.scene.dic_cab[self.condutorLineEdit.currentText()]['rp']))
            self.resistenciaZeroLineEdit.setText(str(self.scene.dic_cab[self.condutorLineEdit.currentText()]['rz']))
            self.reatanciaLineEdit.setText(str(self.scene.dic_cab[self.condutorLineEdit.currentText()]['xp']))
            self.reatanciaZeroLineEdit.setText(str(self.scene.dic_cab[self.condutorLineEdit.currentText()]['xz']))


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Condutor - Propriedades", None, int=-1))
        self.comprimentoLabel.setText(QtWidgets.QApplication.translate("Dialog", "Comprimento", None, int=-1))
        self.resistenciaLabel.setText(QtWidgets.QApplication.translate("Dialog", "Resistencia", None, int=-1))
        self.resistenciaZeroLabel.setText(QtWidgets.QApplication.translate("Dialog", "Resistencia Zero", None, int=-1))
        self.reatanciaLabel.setText(QtWidgets.QApplication.translate("Dialog", "Reatancia", None, int=-1))
        self.reatanciaZeroLabel.setText(QtWidgets.QApplication.translate("Dialog", "Reatancia Zero", None, int=-1))
        self.ampacidadeLabel.setText(QtWidgets.QApplication.translate("Dialog", "Ampacidade", None, int=-1))
        self.condutorLabel.setText(QtWidgets.QApplication.translate("Dialog", "Tipo Condutor", None, int=-1))

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        dialogConductor = ConductorDialog()
        sys.exit(app.exec_())
