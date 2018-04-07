import socket
import zlib
import sys
import hmac

from project_path import PROJECT_PATH

sys.path.insert(0, PROJECT_PATH)

from threading import Thread

from client.manager import manager as client_manager

from client.db.manager import manager as db_manager

from client.base.descriptors import ClientVerifier
from client.base.jimmessage import User
from client.utils.utils import act_time, convert

from client.utils.common import *

import logging
from client.log.log_decor import log
from client.log.log_config import logger_name

logger = logging.getLogger(logger_name)

ACTIONS = ['auth', 'msg', 'get', 'add']


# not used
def client_authenticate(sock, secret_key):
    message = sock.recv(32)
    print('=====', message)
    hash = hmac.new(bytes(secret_key, encoding=CODING), message)
    digest = hash.digest()
    print('==-==', digest)
    sock.send(digest)


class Client(metaclass=ClientVerifier):
    __secret_key = '123456'

    def __init__(self, account_name, password, chat_window=None, host=HOST, port=PORT):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.connect(self.address)

        self._account_name = account_name
        self._password = password
        self.user = User(account_name=account_name, password=password)
        self.chat_window = chat_window

        print('connected {} on port {}'.format(self._account_name, self.sock.getsockname()[1]))

        auth_request = client_manager(self.user, 'auth')
        self.send_byte_request(auth_request)

    @property
    def account_name(self):
        return self._account_name

    @account_name.getter
    def account_name(self):
        return self._account_name

    @property
    def password(self):
        return self._password

    @password.getter
    def password(self):
        return 'Hidden'

    @log(logger)
    def send_byte_request(self, byte_data):
        # print('from <send request>: ', self.sock.getsockname())
        z_bytes = zlib.compress(byte_data)
        try:
            self.sock.send(z_bytes)
            return True
        except TypeError:
            print('wrong data format')
        except OSError:
            print('disconnected')

    @log(logger)
    def get_byte_response(self):
        # client_authenticate(self.sock, self.__secret_key)
        while True:
            # client_authenticate(self.sock, self.__secret_key)
            z_bytes = self.sock.recv(SIZE)
            byte_data = zlib.decompress(z_bytes)
            # print(byte_data)
            if byte_data:
                # вывод в консоль
                # data_to_render = self.parse_byte_data(byte_data)
                # print(data_to_render)
                data = convert(byte_data)
                # print('from client data', data)
                self.render_to_gui(data)

                db_manager(data, self._account_name)

    def render_to_gui(self, data):
        if data['action'] == 'msg':
            data_to_show = self.show_in_chat(data)
            if self.chat_window:
                self.chat_window.print_to_chat(data_to_show)
        elif data['action'] == 'response':  # presence, authenticate
            data_to_show = self.show_in_login(data)
            if self.chat_window:
                self.chat_window.print_to_login(data_to_show)
        elif data['action'] in ('get_contacts', 'contact', 'del_contact', 'add_contact'):
            # data_to_show = self.show_in_contacts(data)
            if self.chat_window:
                # print('to show-->', data_to_show)
                self.chat_window.print_to_contacts(data)

    @staticmethod
    def show_in_chat(data):
        t = act_time(data['time'])
        return '\n{} {} to {}:\n{}\n' \
            .format(t, data['account_name'], data['to'], data['message'])

    @staticmethod
    def show_in_login(data):
        t = act_time(data['time'])
        if 'alert' in data:
            return 'Client added!\n{} {} {}'.format(data['response'], data['alert'], t)
        else:
            if data['response'] == 409:
                return 'Client almost exists! {} {}'.format(data['response'], data['error'])
            elif data['response'] == 500:
                return 'Some trouble on server {} {}'.format(data['response'], data['error'])

    @staticmethod
    def show_in_contacts(data):
        if data['action'] == 'get_contacts':
            return 'You have {} contacts\n'.format(data['quantity'])
        elif data['action'] == 'contact':
            return 'contact {}\n'.format(data['contact'])
        elif data['action'] == 'add_contact':
            return '{} contact {} added'.format(data['response'], data['contact'])
        elif data['action'] == 'del_contact':
            return '{} contact {} deleted'.format(data['response'], data['contact'])

    @staticmethod
    @log(logger)
    def parse_byte_data(byte_data):
        '''
        for console, not used. needed to refactor
        :param byte_data:
        :return:
        '''
        data = convert(byte_data)
        t = act_time(data['time'])
        if data['action'] == 'msg':
            return '***\n{}: <{}> send to <{}> message: {}\n***' \
                .format(t, data['sender'], data['target'], data['message'])
        elif data['action'] == 'response':
            if 'alert' in data:
                return 'code {}, {}!'.format(data['response'], data['alert'])
            else:
                return 'code {}, {}!'.format(data['response'], data['error'])
        else:
            print()
            # TODO сделать парсинг других ответов (data) сервера
            print(data)
            return True

    # mainloop
    def client_action(self, action='msg'):
        '''
        console. not used
        :param action:
        :return:
        '''
        receiver = Thread(target=self.get_byte_response, daemon=True)
        receiver.start()

        while True:
            byte_request = client_manager(self.user, action)
            print('byte request', byte_request)
            if not self.send_byte_request(byte_request):
                break


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('-n', help='account_name')
    # parser.add_argument('-p', help='password')
    # parser.add_argument('-a', help='auth, msg, add, get')
    #
    # args = parser.parse_args()
    #
    # if args.a:
    #     Client(args.n, args.p).client_action(action=args.a)
    # # Client('Marry', '123').client_action()
    # else:
    #     Client(args.n, args.p).client_action()

    Client('Marry', '123').client_action()
