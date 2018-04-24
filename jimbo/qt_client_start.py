import sys
from PyQt5.QtWidgets import QApplication

from .client.gui.main import MyWindow

app = QApplication(sys.argv)
widget = MyWindow()
widget.show()
sys.exit(app.exec_())
