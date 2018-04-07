import sys
from PyQt5.QtWidgets import QApplication
# from subprocess import Popen, CREATE_NEW_CONSOLE

from client.gui.main import MyWindow


app = QApplication(sys.argv)
widget = MyWindow()
widget.show()
sys.exit(app.exec_())


