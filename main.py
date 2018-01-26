from smartpower.gui import simulador
from PySide2 import QtCore, QtGui, QtWidgets
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    mySW = simulador.ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

