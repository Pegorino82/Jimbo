import sys
import os
from project_path import PROJECT_PATH

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication


class LogIn(QtWidgets.QMainWindow):
    acc = 'account'
    pas = 'password'

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(PROJECT_PATH, 'client/gui/log_in.ui'), self)
        self.setWindowTitle('Log in window')
        self.ok_btn.clicked.connect(self.get_auth)
        self.cancel_btn.clicked.connect(self.get_canceled)

    def get_auth(self):
        self.acc = self.account.text()
        self.pas = self.password.text()

        if self.account and self.password:
            with open('acc_pass.txt', 'w') as file:
                file.writelines(self.acc + '\n' + self.pas)
            self.close()
        else:
            self.label_3.setText('wrong account name or password!')

    def get_canceled(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LogIn()
    widget.show()
    sys.exit(app.exec_())
