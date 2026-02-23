import sys
from PyQt6 import QtWidgets

from form_ui import Ui_Widget



class MainWindow(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.ui.ButtonSayHallo.clicked.connect(self.say_hallo)
        self.ui.ButtonPrintHallo.clicked.connect(self.print_hallo)

    def say_hallo(self):
        self.ui.label.setText("Hallo PyQt6 Welt")


    def print_hallo(self):

        self.ui.label_2.setText("Hallo Welt in der Qt6 ")

# ---- start the application ----

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())