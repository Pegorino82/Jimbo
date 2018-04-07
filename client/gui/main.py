import sys
import os
from project_path import PROJECT_PATH

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

from threading import Thread

from client.gui.log_in import LogIn
from client.gui.log_in_exist import LogInExist
from client.gui.contacts import Contacts
from client.client import Client
from client.utils.utils import *
from client.base.jimmessage import User, JIMMessage


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(PROJECT_PATH, 'client/gui/main_window.ui'), self)
        self.setWindowTitle('Messenger')
        self.client = None
        self.user = None
        self.line = None
        self.receiver = None
        self.cont = None

        self.auth_button.clicked.connect(self.auth_pressed)
        self.input_line.returnPressed.connect(self.send_pressed)
        self.contacts_button.clicked.connect(self.contacts)

    def auth_pressed(self):
        if not self.client:
            log_in = LogIn(self)
            log_in.show()
            log_in.ok_btn.clicked.connect(self.get_auth)
        else:
            log_in = LogInExist(self)
            log_in.show()
            time.sleep(5)
            log_in.close()

    def get_auth(self):
        with open('acc_pass.txt', 'r') as file:
            account = file.readline().strip()
            password = file.readline().strip()
        self.account_label.setText(account)

        self.user = User(account_name=account, password=password)
        self.client = Client(account, password, chat_window=self)
        with open('acc_pass.txt', 'w') as file:
            pass

        self.contacts()
        self.cont.close()

        self.chat_show()
        print('get it!')

    def send_pressed(self):
        text = self.input_line.text()
        target = self.comboBox_main_contacts.currentText()
        print('target-->', target)
        byte_message = JIMMessage.msg(self.user, text, target).dump_to_json
        self.client.send_byte_request(byte_message)
        self.input_line.clear()

    def chat_show(self):
        self.receiver = Thread(target=self.client.get_byte_response, daemon=True)
        self.receiver.start()

    def print_to_chat(self, data):
        print('this is for chat', data)
        self.chat_browser.insertPlainText(data)

    def print_to_login(self, data):
        print('to login-->', data)

    def print_to_contacts(self, data):
        if data['action'] == 'contact':
            contact_name = data['contact']
            b = self.comboBox_main_contacts.findText(contact_name)
            if b < 0:
                self.comboBox_main_contacts.addItem(contact_name)
            else:
                print('контакт уже есть в списке')
            b = self.cont.comboBox_contacts.findText(contact_name)
            if b < 0:
                self.cont.comboBox_contacts.addItem(contact_name)
            else:
                print('контакт уже есть в списке')

        elif data['action'] == 'add_contact' and data['response'] == 202:
            contact_name = data['contact']
            b = self.comboBox_main_contacts.findText(contact_name)
            if b < 0:
                self.comboBox_main_contacts.addItem(contact_name)
            b = self.cont.comboBox_contacts.findText(contact_name)
            if b < 0:
                self.cont.comboBox_contacts.addItem(contact_name)

        elif data['action'] == 'del_contact' and data['response'] == 202:
            contact_name = data['contact']
            b = self.cont.comboBox_contacts.findText(contact_name)
            if b >= 0:
                self.cont.comboBox_contacts.removeItem(contact_name)
        print('to contacts-->', data)

    def contacts(self):
        try:
            self.cont = Contacts(self)
            self.cont.show()
            b = self.comboBox_main_contacts.findText('#chat')
            if b < 0:
                self.comboBox_main_contacts.addItem('#chat')
            b = self.cont.comboBox_contacts.findText('#chat')
            if b < 0:
                self.cont.comboBox_contacts.addItem('#chat')
            self.do_get()
            self.cont.pushButton_add.clicked.connect(self.do_add)
            self.cont.pushButton_get.clicked.connect(self.do_get)
            self.cont.pushButton_del.clicked.connect(self.do_del)
        except Exception as err:
            print(err)

    def do_add(self):
        contact_name = self.cont.lineEdit_name.text()
        byte_message = JIMMessage.add_contact(self.user, contact_name).dump_to_json
        self.client.send_byte_request(byte_message)
        self.cont.close()

    def do_get(self):
        byte_request = JIMMessage.get_contacts(self.user).dump_to_json
        self.client.send_byte_request(byte_request)
        # self.cont.close()

    def do_del(self):
        contact_name = self.cont.comboBox_contacts.currentText()
        byte_message = JIMMessage.del_contact(self.user, contact_name).dump_to_json
        self.client.send_byte_request(byte_message)
        index = self.cont.comboBox_contacts.currentIndex()
        self.cont.comboBox_contacts.removeItem(index)
        self.comboBox_main_contacts.removeItem(index)
        self.cont.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())
