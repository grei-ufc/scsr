# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogRecloser.ui'
#
# Created: Sun Feb  8 22:33:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import sys
from smartpower.gui.dialogs.Cadastro import CadastroDialog

class RecloserDialog(QtWidgets.QWidget):

    def __init__(self, item):
        super(RecloserDialog, self).__init__()
        self.dialog = QtWidgets.QDialog(self)
        self.elementTitle = "Interrupção"
        self.item = item
        self.scene = self.item.scene()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        #Dialog.resize(380, 210)
        sc = 10.0
        Dialog.resize(380, 40+33*sc)
        #Define o tamanho da caixa dialogo
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 33*sc, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cadastro = QtWidgets.QPushButton('Cadastrar Novo')
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.addButton(self.cadastro, QtWidgets.QDialogButtonBox.ActionRole)
        self.buttonBox.clicked.connect(self.cadastrar)
        #print self.buttonBox.buttons
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 33*sc))
        #Define a localização do layout das propriedades (coordenada x do ponto, coordenada y do ponto, dimensão em x, dimensão em y)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        # ### Reativar p combo box
        # Definição da COMBOBOX
        self.testeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.testeLabel.setObjectName("testeLabel")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.testeLabel)
        self.testeLineEdit = QtWidgets.QComboBox(self.formLayoutWidget)
        self.testeLineEdit.setObjectName("testeEdit")
        self.testeLineEdit.addItems(list(self.scene.dict_prop.keys()))
        self.testeLineEdit.insertItem(0,"Custom")
        index = self.testeLineEdit.findText(self.item.text_config)
        # if index < 0:
        #     index = 0
        self.testeLineEdit.setCurrentIndex(index)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.testeLineEdit)
        self.testeLineEdit.currentIndexChanged.connect(self.update_values)


        #definição da propriedade NOME
        self.identificaOLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.identificaOLabel.setObjectName("identificaOLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.identificaOLabel)
        self.identificaOLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.identificaOLineEdit.setObjectName("identificaOLineEdit")
        self.identificaOLineEdit.setPlaceholderText(self.item.text.toPlainText())
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.identificaOLineEdit)
        self.identificaOLineEdit.textChanged.connect(self.en_dis_button)

        #definição da propriedade CORRENTE NOMINAL
        self.correnteNominalLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.correnteNominalLabel.setObjectName("correnteNominalLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.correnteNominalLabel)
        self.correnteNominalLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.correnteNominalLineEdit.setObjectName("correnteNominalLineEdit")
        self.correnteNominalLineEdit.setText(str(self.item.chave.ratedCurrent))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.correnteNominalLineEdit)
        self.correnteNominalLineEdit.textEdited.connect(self.custom)


        #definição da propriedade CAPACIDADE DE INTERRUPÇÃO
        self.capacidadeDeInterrupOLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.capacidadeDeInterrupOLabel.setObjectName("capacidadeDeInterrupOLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.capacidadeDeInterrupOLabel)
        self.capacidadeDeInterrupOLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.capacidadeDeInterrupOLineEdit.setObjectName("capacidadeDeInterrupOLineEdit")
        self.capacidadeDeInterrupOLineEdit.setText(str(self.item.chave.breakingCapacity))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.capacidadeDeInterrupOLineEdit)
        self.capacidadeDeInterrupOLineEdit.textEdited.connect(self.custom)


        #definição da propriedade Nº DE SEQUENCIA DE RELIGAMENTO
        self.nDeSequNciasDeReligamentoLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nDeSequNciasDeReligamentoLabel.setObjectName("nDeSequNciasDeReligamentoLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.nDeSequNciasDeReligamentoLabel)
        self.nDeSequNciasDeReligamentoLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nDeSequNciasDeReligamentoLineEdit.setObjectName("nDeSequNciasDeReligamentoLineEdit")
        self.nDeSequNciasDeReligamentoLineEdit.setText(str(self.item.chave.recloseSequences))
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nDeSequNciasDeReligamentoLineEdit)
        self.nDeSequNciasDeReligamentoLineEdit.textEdited.connect(self.custom)

        #definição da propriedade TIPO DE ELEMENTO INTERRUPTOR:

        self.tipoElementoLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.tipoElementoLabel.setObjectName("tipoElementoLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.tipoElementoLabel)

        self.tipoElementoCheck = QtWidgets.QButtonGroup()
        self.tipoElementoCheck.addButton(QtWidgets.QCheckBox(u"Chave",self.formLayoutWidget), 0)
        self.tipoElementoCheck.addButton(QtWidgets.QCheckBox(u"Chave autom.",self.formLayoutWidget), 1)
        self.tipoElementoCheck.addButton(QtWidgets.QCheckBox(u"Disjuntor",self.formLayoutWidget), 2)
        self.tipoElementoCheck.addButton(QtWidgets.QCheckBox(u"Religador",self.formLayoutWidget), 3)
        self.tipoElementoCheck.addButton(QtWidgets.QCheckBox(u"Rel. e TC/TP",self.formLayoutWidget), 4)
        self.tipoElementoCheck.setExclusive(True)

        for item in self.tipoElementoCheck.buttons():
            item.setObjectName("tipoElementoCheck"+str(self.tipoElementoCheck.id(item)))
            self.formLayout.setWidget((4+self.tipoElementoCheck.id(item)), QtWidgets.QFormLayout.FieldRole, item)
            #self.setElementTitle().connect(item.clicked)
            #item.toggled(True).connect(self.setElementTitle())
        self.tipoElementoCheck.button(self.item.chave.tipo).setChecked(True)

        lista_comp = [int(self.capacidadeDeInterrupOLineEdit.text()), int(self.correnteNominalLineEdit.text()), int(self.nDeSequNciasDeReligamentoLineEdit.text())]
        print(lista_comp)

        if self.identificaOLineEdit.text() == "":
            print(self.buttonBox.buttons())
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)
        if self.identificaOLineEdit.placeholderText() != "":
            self.buttonBox.buttons()[0].setEnabled(True)


        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def en_dis_button(self):

        if self.identificaOLineEdit.text() == "":
            print(self.buttonBox.buttons())
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)

    def setElementTitle(self):
        for item in self.tipoElementoCheck.buttons():
            if item.isChecked():
                self.elementTitle = item.text()
        self.retranslateUi(self.dialog)


    def update_values(self, index):

        if index == 0:
            return

        self.correnteNominalLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Corrente Nominal']))
        self.capacidadeDeInterrupOLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Capacidade de Interrupcao']))
        self.nDeSequNciasDeReligamentoLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Sequencia']))


    def custom(self):
        self.testeLineEdit.setCurrentIndex(0)

    def setFormaDialog(self):
        self.dialog.resize(530,370)


    def cadastrar(self, button):
        role = self.buttonBox.buttonRole(button)
        if role == QtWidgets.QDialogButtonBox.ActionRole:


            cadastro = CadastroDialog()
            if cadastro.dialog.result() == 1:
                if cadastro.nomeDoCadastroLineEdit.text() == '':
                    return
                self.scene.create_dict_recloser(
                    self.correnteNominalLineEdit.text(),
                    self.capacidadeDeInterrupOLineEdit.text(),
                    self.nDeSequNciasDeReligamentoLineEdit.text(),
                    cadastro.nomeDoCadastroLineEdit.text())
                self.testeLineEdit.addItem(cadastro.nomeDoCadastroLineEdit.text())
                self.testeLineEdit.setCurrentIndex(self.testeLineEdit.count()-1)



    def teste(self):
        print("teste")


    def retranslateUi(self, Dialog):

        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", self.elementTitle+" - Propriedades", None, int=-1))
        self.identificaOLabel.setText(QtWidgets.QApplication.translate("Dialog", "Identificação:", None, int=-1))
        self.correnteNominalLabel.setText(QtWidgets.QApplication.translate("Dialog", "Corrente Nominal (A): ", None, int=-1))
        self.capacidadeDeInterrupOLabel.setText(QtWidgets.QApplication.translate("Dialog", "Capacidade de Interrupção (kA):", None, int=-1))
        self.nDeSequNciasDeReligamentoLabel.setText(QtWidgets.QApplication.translate("Dialog", "Nº de Sequências de Religamento:", None, int=-1))
        self.tipoElementoLabel.setText(QtWidgets.QApplication.translate("Dialog", "Tipo de elemento interruptor:", None, int=-1))
        self.testeLabel.setText(QtWidgets.QApplication.translate("Dialog", "Fabricante:", None, int=-1))

    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        dialogReligador = RecloserDialog()
        sys.exit(app.exec_())
