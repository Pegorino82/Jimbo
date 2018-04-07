import sys
import os
import time
from sqlite3 import IntegrityError

from project_path import PROJECT_PATH

sys.path.insert(0, PROJECT_PATH)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.db.db_core import Base

from server.db.storage import Storage
from server.db.clients.client import Client
from server.db.clients.contacts import Contact
from server.db.history.history import History
from server.db.messages.messages import Message

DB_FILE_PATH = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'messenger_SQLITE_DB'))


class User:
    def __init__(self, account_name, password, user_info):
        self.account_name = account_name
        self.password = password
        self.user_info = user_info


class DBStorage(Storage):
    """
        в методы передаем параметр типа Client,
        чтобы найти клиента по имени (account_name) - использовать метод find_client
        """

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.engine = create_engine(DB_FILE_PATH)
        Base.metadata.create_all(self.engine)

        self._session_class = sessionmaker(bind=self.engine)

    def add_client(self):
        session = self._session_class()
        new_client = Client(account_name=self.get_user.get('account_name'),
                            password=self.get_user.get('password'),
                            user_info=self.get_user.get('user_info'))
        try:
            session.add(new_client)
            session.commit()
            print('added', new_client.account_name)
            return 202
        # except IntegrityError:
        #     print('failed to add client ->', 409)
        #     return 409
        except Exception as err:
            print('failed to add client ->', err)
            if str(err).find('sqlite3.IntegrityError') > 0:
                return 409
            else:
                return 500

    def add_contact(self):
        session = self._session_class()
        ow = session.query(Client).filter(Client.account_name == self.get_user.get('account_name')).first()
        co = session.query(Client).filter(Client.account_name == self.get_contact.get('to')).first()
        contact_list = session.query(Contact).filter(Contact.owner_id == ow.client_id).all()
        if co:
            if co.client_id in [co.contact_id for co in contact_list]:
                print('contact almost exists')
                return 409
            else:
                new_contact = Contact(owner_id=ow.client_id, contact_id=co.client_id)
                try:
                    session.add(new_contact)
                    session.commit()
                    print('added contact', co.account_name)
                    return 202
                except Exception as err:
                    print('failed to add contact ->', err)
                    return 500
        else:
            return 404

    def del_contact(self):
        owner = self.get_user.get('account_name')
        session = self._session_class()
        ow = session.query(Contact).filter(Contact.owner_id == self.find_client(owner).client_id).first()
        co = session.query(Client).filter(Client.account_name == self.get_contact.get('to')).first()
        # print('co-->', co.client_id)
        contact_list = session.query(Contact).filter(Contact.owner_id == ow.owner_id).all()
        # print('c_list-->', contact_list)
        if co:
            for p in contact_list:
                # print('cont id-->', p.contact_id)
                if co.client_id == p.contact_id:
                    try:
                        session.delete(p)
                        session.commit()
                        print('deleted', co.account_name)
                        return 202
                    except Exception as err:
                        print('failed to del contact ->', err)
                        return 500
                # else:
                #     return 404
        else:
            return 404

    def get_contacts(self):
        session = self._session_class()
        cont_list = list()
        ow = session.query(Client).filter(Client.account_name == self.get_user.get('account_name')).first()
        que = session.query(Contact).filter(Contact.owner_id == ow.client_id).all()
        for cont in que:
            contact = session.query(Client).filter(Client.client_id == cont.contact_id).first()
            cont_list.append(contact.account_name)
        return cont_list

    def find_client(self, account_name):
        # print('ищу клиента')
        session = self._session_class()
        try:
            client = session.query(Client).filter(Client.account_name == account_name).first()
            return client
        except Exception as err:
            print('no such client ->', err)

    def add_message(self):
        session = self._session_class()
        time_ = time.time()
        client = self.get_user.get('account_name')
        target = self.get_contact.get('to')
        message = self.get_message.get('message')
        cl = session.query(Client).filter(Client.account_name == client).first()
        try:
            tar = session.query(Client).filter(Client.account_name == target).first()
            target = tar.client_id
        except:
            pass
        new_message = Message(message_time=time_, client_id=cl.client_id, target_id=target, message=message)
        try:
            session.add(new_message)
            session.commit()
        except Exception as err:
            print('failed to add message ->', err)

    def add_to_history(self):
        session = self._session_class()
        user = self.get_user.get('account_name')
        action = self.get_action.get('action')
        time_ = time.time()
        client = self.find_client(user)

        history = History(time=time_, client_id=client.client_id, action=action)
        try:
            session.add(history)
            session.commit()
            print('added to history {} {}'.format(client.client_id, history.action))
        except Exception as err:
            print('failed adding to history {} ->'.format(client.client_id), err)


if __name__ == "__main__":
    # client_1 = User(account_name='User_1', password='pass_1', user_info='User_1 info')
    # client_2 = User(account_name='User_2', password='pass_2', user_info='User_2 info')
    # client_3 = User(account_name='User_3', password='pass_3', user_info='User_3 info')
    # print(type(client_1))
    # print(client_1.account_name)

    cli_1 = {'action': 'presence', 'user': {'account_name': 'Cli_1', 'password': '123'}}
    cli_2 = {'action': 'presence', 'user': {'account_name': 'Cli_2', 'password': '123'}}
    cli_3 = {'action': 'presence', 'user': {'account_name': 'Cli_3', 'password': '123'}}
    cli_4 = {'action': 'presence', 'user': {'account_name': 'Cli_4', 'password': '123'}}

    msg = {'action': 'msg', 'to': '#chat', 'message': 'testtext', 'time': 1520535974.6585314, 'account_name': 'Cli_1'}

    add_1 = {'action': 'add_contact', 'account_name': 'Cli_1', 'time': 1521551226.1956553, 'to': 'Cli_2'}
    add_2 = {'action': 'add_contact', 'account_name': 'Cli_1', 'time': 1521551226.1956553, 'to': 'Cli_3'}

    del_1 = {'action': 'del_contact', 'account_name': 'Cli_1', 'time': 1521551226.1956553, 'to': 'Cli_3'}
    del_2 = {'action': 'del_contact', 'account_name': 'Cli_1', 'time': 1521551226.1956553, 'to': 'Cli_2'}

    get_1 = {'action': 'get_contacts', 'account_name': 'Cli_1', 'time': 1521551226.1956553}

    db_1 = DBStorage(cli_1)
    db_1.add_client()

    db_2 = DBStorage(cli_2).add_client()
    db_3 = DBStorage(cli_3).add_client()
    db_4 = DBStorage(cli_4).add_client()
    #
    db_add_1 = DBStorage(add_1).add_contact()
    db_add_2 = DBStorage(add_2).add_contact()

    # db_del = DBStorage(del_1).del_contact()
    # db_del = DBStorage(del_2)
    # db_del.del_contact()
    # db_del.add_to_history()

    db_get_1 = DBStorage(get_1).get_contacts()
    print(db_get_1)

    # db_hist_1 = DBStorage(del_1).del_contact()
