#! /usr/bin/python
# -*- coding: utf-8 -*-

# Criado em: Sun Jan 26 16:58:45 2014
#        por: Lucas S Melo
#

from PySide2 import QtCore, QtGui, QtWidgets
from smartpower.core.graphics import SceneWidget, ViewWidget
from smartpower.core.cursor import Cursor
import sys
import os
import smartpower.core.models as models


class JanelaPrincipal(object):
    '''
        Esta classe implementa a interface grafica do simulador
    '''

    def __init__(self):
        self.cursor = Cursor("")
        pass

    def inicializar_componentes(self, main_window):
        '''
            Este metodo implementa os componentes da interface grafica
        '''

        # define a janela pricipal do aplicativo
        main_window.setObjectName('main_window')
        main_window.setWindowIcon(QtGui.QIcon('icones/carc2.png'))
        main_window.resize(900, 700)

        # define o widget central do aplicativo
        self.centralwidget = QtWidgets.QTabWidget(main_window)
        self.centralwidget.setObjectName('centralwidget')

        # define o tipo de layout do widget central como gridLayout
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName('gridLayout')

        # define a classe SceneWidget e ViewWidget como containers dos widgets
        self.sceneWidget = SceneWidget(self)
        self.graphicsView = ViewWidget(self.sceneWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(256, 0))
        self.graphicsView.setObjectName('graphicsView')
        self.centralwidget.addTab(self.graphicsView,'Diagrama')

        # adiciona os sinais ao objeto sceneWidget
        self.sceneWidget.itemInserted.connect(self.itemInserted)
        # conecta os botoes aos signals da sceneWidget
        # self.sceneWidget.InsertItem.connect(self.itemInserted)

        # seta o objeto QGraphicsView no gridLayout
        #self.gridLayout.addWidget(self.graphicsView, 0, 0)
        main_window.setCentralWidget(self.centralwidget)

        # define a barra de menus
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(0, 0, 600, 25)
        self.menubar.setObjectName("menubar")
        #main_window.setMenuBar(self.menubar)
        
        

        #Cria os Menu e Submenus na barra de menu
        self.fileMenu = self.menubar.addMenu('Arquivo')
        self.showMenu = self.menubar.addMenu('Exibir')
        self.orgMenu = self.menubar.addMenu('Organizar')

        self.simulationMenu = self.menubar.addMenu(u'Simulação')
        self.helpMenu = self.menubar.addMenu('Ajuda')
        #Cria o submenu Alinhar e o coloca no menu Organizar
        self.alignSubmenu = self.orgMenu.addMenu('Alinhar')
        #Cria o submenu Texto e o coloca no menu Organizar
        self.textSubmenu = self.showMenu.addMenu('Texto')


        # define a barra de status
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)


        # define o widget dockWidget dockWidget_Buttons e configura seu
        # conteudo dockWidget_Buttons_Contents
        self.dockWidget_Buttons = QtWidgets.QDockWidget(main_window)
        self.dockWidget_Buttons.setCursor(self.cursor)
        self.dockWidget_Buttons.setObjectName("dockWidget_Buttons")
        self.dockWidget_Buttons_Contents = QtWidgets.QWidget()
        self.dockWidget_Buttons_Contents.setFixedWidth(65)
        self.dockWidget_Buttons_Contents.setObjectName(
            "dockWidget_Buttons_Contents")

        #  define o layput dos botoes no dockWidget  gridLayout
        self.gridLayout_dockWidget = QtWidgets.QGridLayout(
            self.dockWidget_Buttons_Contents)
        self.gridLayout_dockWidget.setObjectName("gridLayout_dockWidget")

        # define o objeto QToolBox que comportara as abas de botoes
        self.toolBox = QtWidgets.QToolBox(self.dockWidget_Buttons_Contents)
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setObjectName("toolBox")

        # define a primeira pagina do dockWidget
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 100, 50))

        # configura a primeira pagina do dockWidget
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.page_1.sizePolicy().hasHeightForWidth())
        self.page_1.setSizePolicy(size_policy)
        self.page_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.page_1.setAutoFillBackground(True)
        self.page_1.setObjectName("page_1")

        # define o Layout da primeira pagina do dockWidget
        self.gridlayout_page_1 = QtWidgets.QGridLayout(self.page_1)
        self.gridlayout_page_1.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridlayout_page_1.setObjectName("gridlayout_page_1")

        # define os botoes da primeira pagina do dockWidget e insere no
        # FormLayout

        self.iconSubstation = QtGui.QIcon("icones/iconTrafo.png")
        self.iconBus = QtGui.QIcon("icones/iconBus.png")
        self.iconRecloser = QtGui.QIcon("icones/iconRecloser.png")
        self.iconLine = QtGui.QIcon("icones/iconLine.png")
        self.iconNode = QtGui.QIcon("icones/iconNode.png")
        self.icontam = QtCore.QSize(30,30)
        self.substationButton = QtWidgets.QToolButton(self.page_1)
        self.substationButton.setIcon(self.iconSubstation)
        self.substationButton.setIconSize(self.icontam)
        self.substationButton.setObjectName("substationButton")
        self.substationButton.setCheckable(True)
        self.busButton = QtWidgets.QToolButton(self.page_1)
        self.busButton.setIcon(self.iconBus)
        self.busButton.setIconSize(self.icontam)
        self.busButton.setObjectName("busButton")
        self.busButton.setCheckable(True)
        self.recloserButton = QtWidgets.QToolButton(self.page_1)
        self.recloserButton.setIcon(self.iconRecloser)
        self.recloserButton.setIconSize(self.icontam)
        self.recloserButton.setObjectName("recloserButton")
        self.recloserButton.setCheckable(True)
        self.lineButton = QtWidgets.QToolButton(self.page_1)
        self.lineButton.setIcon(self.iconLine)
        self.lineButton.setIconSize(self.icontam)
        self.lineButton.setObjectName("lineButton")
        self.lineButton.setCheckable(True)
        self.noButton = QtWidgets.QToolButton(self.page_1)
        self.noButton.setIcon(self.iconNode)
        self.noButton.setIconSize(self.icontam)
        self.noButton.setObjectName("noButton")
        self.noButton.setCheckable(True)


        # define o grupo de botoes da pagina 1 do notebook
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.addButton(self.substationButton, 0)
        self.buttonGroup.addButton(self.recloserButton, 1)
        self.buttonGroup.addButton(self.busButton, 2)
        self.buttonGroup.addButton(self.lineButton, 3)
        self.buttonGroup.addButton(self.noButton, 4)
        self.buttonGroup.setExclusive(False)

        self.buttonGroup.buttonClicked[int].connect(self.buttonGroupClicked)
        self.buttonGroup.buttonClicked[int].connect(main_window.setCursorPad)
        self.buttonGroup.buttonPressed[int].connect(self.buttonGroupPressed)
        self.buttonGroup.buttonPressed[int].connect(main_window.setCursorIcon)
        self.buttonGroup.buttonReleased[int].connect(self.buttonGroupReleased)
        self.buttonGroup.buttonReleased[int].connect(main_window.setCursorIcon)

        # define labels da primeira pagina do dockWidget
        self.substationLabel = QtWidgets.QLabel('')
        self.substationLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.substationLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.substationLabel.setObjectName("substationLabel")
        self.recloserLabel = QtWidgets.QLabel('')
        self.recloserLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.recloserLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.recloserLabel.setObjectName("recloserLabel")
        self.busLabel = QtWidgets.QLabel('')
        self.busLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.busLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.busLabel.setObjectName("busLabel")
        self.lineLabel = QtWidgets.QLabel('')
        self.lineLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lineLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lineLabel.setObjectName("lineLabel")
        self.noLabel = QtWidgets.QLabel('')
        self.noLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.noLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.noLabel.setObjectName("noLabel")

        # adiciona os botoes ao gridLayout_3
        self.gridlayout_page_1.addWidget(self.substationButton, 0, 0)
        self.gridlayout_page_1.addWidget(self.recloserButton, 2, 0)
        self.gridlayout_page_1.addWidget(self.substationLabel, 1, 0)
        self.gridlayout_page_1.addWidget(self.recloserLabel, 3, 0)
        self.gridlayout_page_1.addWidget(self.busButton, 4, 0)
        self.gridlayout_page_1.addWidget(self.lineButton, 6, 0)
        self.gridlayout_page_1.addWidget(self.busLabel, 5, 0)
        self.gridlayout_page_1.addWidget(self.lineLabel, 7, 0)
        self.gridlayout_page_1.addWidget(self.noButton, 8, 0)
        self.gridlayout_page_1.addWidget(self.noLabel, 9, 0)

        # adiciona o gridLayout_3 a pagina_1 do dockWidget
        self.page_1.setLayout(self.gridlayout_page_1)

        # seta a primeira pagina do dockWidget
        self.toolBox.addItem(self.page_1, "")

        # define a segunda pagina do dockWidget
        # self.page_2 = QtWidgets.QWidget()
        # self.page_2.setGeometry(QtCore.QRect(0, 0, 100, 50))
        # self.page_2.setObjectName("page_2")
        # self.toolBox.addItem(self.page_2, "")

        self.gridLayout_dockWidget.addWidget(self.toolBox, 0, 0)
        self.dockWidget_Buttons.setWidget(self.dockWidget_Buttons_Contents)

        main_window.addDockWidget(
            QtCore.Qt.DockWidgetArea(1), self.dockWidget_Buttons)

        # configura os botoes da barra de ferramentas

        # cria e configura acao de sair do programa
        self.actionExit = QtWidgets.QAction(main_window)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setShortcut('Ctrl+Q')
        #self.toolBar.addAction(self.actionExit)
        self.fileMenu.addAction(self.actionExit)

        # cria e configura acao de salvar o estado atual do programa
        self.actionSave = QtWidgets.QAction(
            main_window, triggered=self.save)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut('Ctrl+S')
        #self.toolBar.addAction(self.actionSave)
        self.fileMenu.addAction(self.actionSave)

        # cria e configura acao de abrir um arquivo com uma configuração da
        # rede montada anteriormente
        self.actionOpen = QtWidgets.QAction(main_window, triggered=self.open)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut('Ctrl+A')
        #self.toolBar.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionOpen)

        # cria e configura acao de inserir ou retirar grade no diagrama grafico
        self.actionGrid = QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.set_grid)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionGrid")
        self.actionGrid.setShortcut('Ctrl+G')
        #self.toolBar.addAction(self.actionGrid)
        self.showMenu.addAction(self.actionGrid)

        # cria e configura ação de alinhar horizontalmente itens no diagrama
        # gráfico
        self.actionHalign = QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.h_align)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionHalign")
        self.actionHalign.setShortcut('Ctrl+H')
        #self.toolBar.addAction(self.actionHalign)
        self.alignSubmenu.addAction(self.actionHalign)

        # cria e configura ação de alinhar verticalmente items no diagrama
        # gráfico
        self.actionValign = QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.v_align)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionValign")
        self.actionValign.setShortcut('Ctrl+V')
        #self.toolBar.addAction(self.actionValign)
        self.alignSubmenu.addAction(self.actionValign)

        # cria e configura acao de selecionar items no diagrama grafico
        self.actionSelect = QtWidgets.QAction(
            main_window, triggered=self.setSelect)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon)
        self.actionSelect.setObjectName("actionSelect")
        self.actionSelect.setShortcut('Ctrl+E')
        #self.toolBar.addAction(self.actionSelect)
        self.orgMenu.addAction(self.actionSelect)

        # cria e configura ação de abrir a interface de simulação
        
        self.action_simulate = QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.simulate)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionSimulate")
        self.action_simulate.setShortcut('Ctrl+M')
        #self.toolBar.addAction(self.action_simulate)
        self.simulationMenu.addAction(self.action_simulate)

                #### teste
        self.choice_simulate_1 = QtWidgets.QAction(
            main_window, triggered=self.simulate)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon)
        self.actionSelect.setObjectName("choiceSimulate1")
        #self.choice_simulate_1.setShortcut('Ctrl+M')
        #self.toolBar.addAction(self.action_simulate)
        self.simulationMenu.addAction(self.choice_simulate_1)


        # cria e configura a acao de tornar o texto visível ou não
        ### subestação
        self.actionTextVisibleSubstation = QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.setTextSubstation, checkable=True ,checked=True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTextVisibleSubstation.setIcon(icon)
        self.actionTextVisibleSubstation.setObjectName("actionTextVisibleSubstation")
        self.textSubmenu.addAction(self.actionTextVisibleSubstation)
        ### religador
        self.actionTextVisibleRecloser =QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.setTextRecloser, checkable=True ,checked=True)
        self.actionTextVisibleRecloser.setIcon(icon)
        self.actionTextVisibleRecloser.setObjectName("actionTextVisibleRecloser")
        self.textSubmenu.addAction(self.actionTextVisibleRecloser)
        ### barra
        self.actionTextVisibleBus =QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.setTextBus, checkable=True ,checked=True)
        self.actionTextVisibleBus.setIcon(icon)
        self.actionTextVisibleBus.setObjectName("actionTextVisibleBus")
        self.textSubmenu.addAction(self.actionTextVisibleBus)
        ### no de carga
        self.actionTextVisibleNodeC =QtWidgets.QAction(
            main_window, triggered=self.sceneWidget.setTextNodeC, checkable=True ,checked=True)
        self.actionTextVisibleNodeC.setIcon(icon)
        self.actionTextVisibleNodeC.setObjectName("actionTextVisibleNodeC")
        self.textSubmenu.addAction(self.actionTextVisibleNodeC)

        # configurações adicionais
        self.retranslateUi(main_window)
        #self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def itemInserted(self, item_type):
        '''
            Callback chamada no momento em que um item e inserido
            no diagrama grafico
        '''
        if item_type != 3:

            self.buttonGroup.button(item_type).setChecked(False)
            self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
            self.dockWidget_Buttons.setCursor(Cursor(""))
            self.centralwidget.setCursor(Cursor(""))

        else:
            pass
        

    def save(self):
        '''
            Função que salva o diagrama gráfico em um arquivo .XML
        '''
        filename = QtWidgets.QFileDialog.getSaveFileName(
            None, 'Salvar Diagrama', os.getenv('HOME'))
        file = models.DiagramToXML(self.sceneWidget)
        file.write_xml(filename[0])
        filename_CIM = filename[0] + '_CIM.xml'

        file2 = models.CimXML(self.sceneWidget)
        file2.write_xml(filename_CIM)

        return filename_CIM

    def simulate(self):
        bridge=models.start_conversion(self.sceneWidget)
        self.sceneWidget.simulate_1(bridge)
        pass


    def open(self):
        '''
            Função que redesenha um diagrama gráfico que foi salvo anteriormente em um arquivo .XML
        '''
        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Abrir Diagrama', os.getenv('HOME'))
        file = models.XMLToDiagram(self.sceneWidget, filename[0])

    def setSelect(self):
        '''
            Callback chamada no momento em que se faz necessario
            alterar do modo de selecao para movimentacao de items
            no diagrama grafico ou vice-versa
        '''
        if self.sceneWidget.myMode == self.sceneWidget.SelectItems:
            self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
        else:
            self.sceneWidget.set_mode(self.sceneWidget.SelectItems)

        for id in range(6):
            self.buttonGroup.button(id).setChecked(False)

        

    def buttonGroupClicked(self, id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é clicado.
        '''
        self.buttonGroup.button(id).setChecked(True)

        # Altera o icone de acordo com o button pressionado:

        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)
        if id==3:
           self.buttonGroup.button(id).setChecked(True)
        
        else:
            self.buttonGroup.button(id).setChecked(False)
            self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
            self.dockWidget_Buttons.setCursor(Cursor(""))
            self.centralwidget.setCursor(Cursor(""))

        

    def buttonGroupPressed(self, id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é pressionado.
        '''

        self.buttonGroup.button(id).setChecked(True)

        # Altera o icone de acordo com o button pressionado:

        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)

        # Altera o modo para: inserir linha, inserir item ou mover item.



        if id == 3:
            self.sceneWidget.set_mode(SceneWidget.InsertLine)
        else:
            self.sceneWidget.set_item_type(id)
            self.sceneWidget.set_mode(SceneWidget.InsertItem)

        self.dockWidget_Buttons.setCursor(Cursor(""))






    def buttonGroupReleased(self,id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é liberado.

'''
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)

        # if self.buttonGroup.button(id) != QtCore.Qt.LeftButton:
        #     self.dockWidget_Buttons.setCursor(Cursor(""))
        #     self.centralwidget.setCursor(Cursor(""))
        if id == 3:
            self.sceneWidget.set_mode(SceneWidget.InsertLine)
        else:
            
            self.sceneWidget.set_item_type(id)
            self.sceneWidget.set_mode(SceneWidget.InsertItem)



    def buttonGroupUncheck(self):
        '''
            Callback chamada para remover a seleção de todos os buttons.
        '''
        buttons = self.buttonGroup.buttons()

        for button in buttons:
            button.setChecked(False)

        self.sceneWidget.set_mode(SceneWidget.MoveItem)

    def retranslateUi(self, main_window):

        main_window.setWindowTitle(QtWidgets.QApplication.translate(
            "main_window", "Smart Power v0.2 - Simulador de Redes Elétricas de Distribuição",
            None, int=-1))


        self.substationButton.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Transformador", None,
                int=-1))

        self.busButton.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Barra", None, int=-1))

        self.busLabel.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Barra", None, int=-1))

        self.substationLabel.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Trafo", None,
                int=-1))

        self.recloserButton.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Elemento Interruptor", None,
                int=-1))

        self.recloserLabel.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Chaves", None,
                int=-1))

        self.lineButton.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Linha", None, int=-1))

        self.lineLabel.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Linha", None, int=-1))

        self.noButton.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Nó de Carga", None, int=-1))

        self.noLabel.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Nó de \n Carga", None, int=-1))

        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_1),
            QtWidgets.QApplication.translate(
                "main_window", "", None,
                int=-1))

        # self.toolBox.setItemText(
        #     self.toolBox.indexOf(self.page_2), QtWidgets.QApplication.translate(
        #         "main_window", "Pagina 2", None,
        #         int=-1))

        self.actionExit.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Sair", None, int=-1))

        self.actionExit.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Sair", None, int=-1))
        '''
        self.actionExit.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "4, Backspace", None,
                int=-1))
        '''
        self.actionSave.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Salvar", None, int=-1))

        self.actionSave.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Salvar", None, int=-1))
        '''
        self.actionSave.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "4, Ctrl + S", None,
                int=-1))
        '''
        self.actionOpen.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Abrir", None, int=-1))

        self.actionOpen.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Abrir", None, int=-1))
        '''
        self.actionOpen.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "4, Ctrl + A", None,
                int=-1))
        '''
        self.actionGrid.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Grade", None, int=-1))

        self.actionGrid.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Grade", None, int=-1))
        '''
        self.actionGrid.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "Ctrl, g", None,
                int=-1))
        '''
        self.actionHalign.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Horizontalmente", None,
                int=-1))

        self.actionHalign.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Alinha Horizontalmente", None,
                int=-1))
        '''
        self.actionHalign.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "Ctrl, h", None,
                int=-1))
        '''
        self.actionValign.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Verticalmente", None,
                int=-1))

        self.actionValign.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Alinha Verticalmente", None,
                int=-1))
        '''
        self.actionValign.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "Ctrl, h", None,
                int=-1))
        '''
        self.actionSelect.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Selecionar Items", None,
                int=-1))

        self.actionSelect.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Selecionar Items", None,
                int=-1))
        '''
        self.actionSelect.setShortcut(
            QtWidgets.QApplication.translate(
                "main_window", "Ctrl, e", None,
                int=-1))
        '''
        self.action_simulate.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Simular", None,
                int=-1))
            

        self.action_simulate.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Simular", None,
                int=-1))

        self.choice_simulate_1.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Simular_curto", None,
                int=-1))

        self.choice_simulate_1.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Simular_curto", None,
                int=-1))

        ## Configuração das QActions para exibir textos dos elementos, sem atalhos.
        self.actionTextVisibleSubstation.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Subestações", None, int=-1))

        self.actionTextVisibleSubstation.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Subestação", None, int=-1))

        self.actionTextVisibleRecloser.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Religadores", None, int=-1))

        self.actionTextVisibleRecloser.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Religador", None, int=-1))

        self.actionTextVisibleBus.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Barras", None, int=-1))

        self.actionTextVisibleBus.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Religador", None, int=-1))

        self.actionTextVisibleNodeC.setText(
            QtWidgets.QApplication.translate(
                "main_window", "Nós de Carga", None, int=-1))

        self.actionTextVisibleNodeC.setToolTip(
            QtWidgets.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Nó de Carga", None, int=-1))


class ControlMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.cursor = Cursor("")
        self.setCursor(self.cursor)
        self.ui = JanelaPrincipal()
        self.ui.inicializar_componentes(self)

    def mouseReleaseEvent(self, mouse_event):
        '''
            Função da chamada no momento que o evento mouse release é enviado. Quando um
            item arrastado para a área de desenho é liberado, este item é desenhado e o
            programa volta para o modo de seleção de itens.
        '''
        self.setCursorPad(1)
        super(ControlMainWindow, self).mouseReleaseEvent(mouse_event)
        sinal = QtWidgets.QGraphicsSceneMouseEvent(QtCore.QEvent.GraphicsSceneMouseRelease)
        sinal.setPos(self.ui.graphicsView.mapToScene(
            self.ui.graphicsView.mapFromGlobal(self.cursor.pos())))
        self.ui.sceneWidget.mouseReleaseEvent(sinal)
        self.ui.buttonGroupUncheck()

    def setCursorIcon(self, id):
        '''
            Callback que altera o formato do cursor dando a impressão visual de
            'arrastar' o elemento para dentro do diagrama gráfico.
        '''

        self.cursor.setShape(self, id)
        self.ui.cursor.setShape(self.ui.dockWidget_Buttons, id)

    def setCursorPad(self, id):
        '''
            Função que altera o formato do cursor para a seta padrão.
        '''
        self.cursor.setShapePad(self)
        self.ui.cursor.setShapePad(self.ui.dockWidget_Buttons)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
