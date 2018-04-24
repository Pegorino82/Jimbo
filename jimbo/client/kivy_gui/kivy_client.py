print('kivy client imported')
import time
from threading import Thread
from ..project_path import PROJECT_PATH

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, StringProperty

from ..client import Client
from ..base.jimmessage import JIMMessage, User
from ..utils.utils import convert
print('kivy client flag 1')

class ContactsWidget(ListItemButton):

    # contact button in contacts list
    def print_contact(self):
        print(self.cont)


class ChatWidget(Widget):
    pass


class LoginWidget(Widget):
    pass


class MainWidget(Widget):
    contact_list = ObjectProperty()
    selected_name = StringProperty('')

    def __init__(self, *args):
        super().__init__()
        self.account_name = None
        self.password = None

        self.client = None
        self.user = None
        self.receiver = None

    def send_press(self):
        data = self.ids.message_line.text
        target = self.selected_name or self.ids.contact_line.text

        print('target:', target)

        if not target or target not in self.ids.list_contacts.item_strings:
            self.ids.contact_line.text = ''
            target = '#chat'

        message = JIMMessage.msg(self.client.user, data, target).jim_dict
        byte_message = convert(message)
        self.client.send_byte_request(byte_message)
        self.ids.message_line.text = ''

    def render_in_chat(self):
        self.receiver = Thread(target=self.client.get_byte_response, daemon=False)
        self.receiver.start()
        # self.receiver.join(0.5)

    def print_to_chat(self, data):
        print('this is for chat', data)
        self.ids.chat_label.text += data + '\n'

    def print_to_login(self, data):
        print('to login-->', data)
        if data == 'Failed to authenticate!':
            self.client.sock.close()
            self.ids.account.text = ''
            self.ids.password.text = ''

    def print_to_contacts(self, data):
        if data['action'] == 'contact' or (data['action'] == 'add_contact' and data['response'] == 202):
            contact_name = data['contact']
            if contact_name not in self.ids.list_contacts.item_strings:
                self.ids.list_contacts.item_strings.append(contact_name)
        elif data['action'] == 'del_contact' and data['response'] == 202:
            contact_name = data['contact']
            self.ids.contact_line.text = ''
            if contact_name in self.ids.list_contacts.item_strings:
                self.ids.list_contacts.item_strings.remove(contact_name)

    def get_login(self):
        self.account_name = self.ids.account.text
        self.password = self.ids.password.text
        self.user = User(account_name=self.account_name, password=self.password)
        self.client = Client(self.account_name, self.password, chat_window=self)
        self.render_in_chat()
        time.sleep(0.5)
        self.refresh_contacts()

    def get_cancel(self):
        # close app
        self.ids.account.text = ''
        self.ids.password.text = ''
        self.ids.contact_line.text = ''
        self.ids.list_contacts.item_strings = ['#']
        self.client.sock.close()
        print('fields cleared\nclose app')

    def add_contact(self):
        contact = self.ids.contact_line.text
        byte_message = JIMMessage.add_contact(self.user, contact).dump_to_json
        self.client.send_byte_request(byte_message)
        print('send add_contact request', contact)

    def del_contact(self):
        contact = self.ids.contact_line.text
        byte_message = JIMMessage.del_contact(self.user, contact).dump_to_json
        self.client.send_byte_request(byte_message)
        print('send del_contact request', contact)

    def refresh_contacts(self):
        byte_request = JIMMessage.get_contacts(self.user).dump_to_json
        print('sending contacts request-->', convert(byte_request))
        self.client.send_byte_request(byte_request)
        print('sended!')

    def cont(self, name):
        print('name:', name)
        self.selected_name = name
        self.ids.contact_line.text = ''
        self.ids.contact_line.insert_text(name)


class ClientApp(App):

    def build(self):
        return MainWidget()


if __name__ == '__main__':
    ClientApp().run()
