import sys
import os
from ..project_path import PROJECT_PATH

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication


class Contacts(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(PROJECT_PATH, 'gui/contacts.ui'), self)
        self.setWindowTitle('Contacts')

    def get_canceled(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Contacts()
    widget.show()
    sys.exit(app.exec_())
