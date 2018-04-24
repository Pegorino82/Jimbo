import sys
import os
from ..project_path import PROJECT_PATH

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication


class LogInExist(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(PROJECT_PATH, 'gui/log_in_exist.ui'), self)
        self.setWindowTitle('info')
        self.label_info.setText('You are already in!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LogInExist()
    widget.show()
    sys.exit(app.exec_())
