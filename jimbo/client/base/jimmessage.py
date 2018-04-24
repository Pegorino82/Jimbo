import json
import time

from .descriptors import MetaJIMMessage, FieldType
from ..utils.common import *
from ..utils.utils import convert


class Group:
    group_name = FieldType('group_name', TARGET, str, 25)

    __slots__ = {group_name.name}

    def __init__(self, group_name):
        self._group_name = '#' + group_name


class User:
    account_name = FieldType('account_name', ACCOUNT_NAME, str, 25)
    password = FieldType('password', PASSWORD, (str, int), 25)
    user_info = FieldType('user_info', USERNAME, str, 25)

    __slots__ = {account_name.name, password.name, user_info.name}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def user_dict(self):
        jim_dict = {}
        for key in self.__slots__:
            try:
                value = getattr(self, key)
                jim_dict[key] = value
            except:
                pass
        return jim_dict


class JIMMessage(metaclass=MetaJIMMessage):
    # action = FieldType('action', ACTIONS[0], str, 15)  # 'presence' by default
    # message = FieldType('message', DEFAULT_TEXT, (str, int), 500)  # 'default text' by default
    # type = FieldType('type', TYPES[0], str, 6)  # 'text' by default
    # encoding = FieldType('encoding', CODING, str, 10)  # 'utf-8' by default
    # room = FieldType('room', TARGET, str, 25)  # '#test_chat_room' by default
    # status = FieldType('status', STATUS_MESSAGE, str, 15)
    # user = FieldType('user', ACCOUNT_NAME, str, 25)
    # account_name = FieldType('account_name', ACCOUNT_NAME, str, 25)
    # password = FieldType('password', PASSWORD, (str, int), 25)
    # username = FieldType('username', USERNAME, str, 25)
    # time = FieldType('time', '', float, 25)  # определиться с типом
    # sender = FieldType('sender', '', str, 25)
    # target = FieldType('target', TARGET, str, 25)  # '#test_chat_room' by default

    # __slots__ = {action.name, message.name, target.name, type.name, encoding.name, room.name, status.name, sender.name,
    #              time.name, user.name, account_name.name, password.name, username.name, sender.name}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def presence(user):
        """
        :param user: instance of User class
        :return: instance of JIMMessage
        """
        time_ = time.time()
        user = {'account_name': user.account_name, 'user_info': user.user_info}
        return JIMMessage(action='presence', type='status', time=time_, user=user)

    @staticmethod
    def probe_answer(user):
        """
        :param user: instance of User class
        :return:
        """
        return JIMMessage.presence(user)

    @staticmethod
    def authenticate(user):
        """
        :param user: instance of User class
        :return: instance of JIMMessage
        """
        time_ = time.time()
        user = {'account_name': user.account_name, 'password': user.password}
        # user = user.user_dict
        return JIMMessage(action='authenticate', time=time_, user=user)

    @staticmethod
    def msg(user, text, to):
        '''
        to: target
        :param user: User instance
        :param text: string text
        :return:
        '''
        time_ = time.time()
        account_name = user.account_name
        message = text
        if isinstance(to, Group):
            to = to.group_name
        elif isinstance(to, User):
            to = to.account_name
        else:
            to = to
        return JIMMessage(action='msg', time=time_, account_name=account_name, to=to, message=message, encoding=CODING)

    @staticmethod
    def get_contacts(user):
        return JIMMessage(action='get_contacts', account_name=user.account_name, time=time.time())

    @staticmethod
    def add_contact(user, to):
        '''
        :param user: User instance
        :param to: User instance
        :return:
        '''
        time_ = time.time()
        account_name = user.account_name
        if isinstance(to, User):
            to = to.account_name
        else:
            to = to
        return JIMMessage(action='add_contact', time=time_, account_name=account_name, to=to)

    @staticmethod
    def del_contact(user, to):
        time_ = time.time()
        account_name = user.account_name
        if isinstance(to, User):
            to = to.account_name
        else:
            to = to
        return JIMMessage(action='del_contact', time=time_, account_name=account_name, to=to)

    @staticmethod
    def get_contacts(user):
        time_ = time.time()
        account_name = user.account_name
        return JIMMessage(action='get_contacts', time=time_, account_name=account_name)

    @staticmethod
    def join(user, group):
        """
        :param group: instance of Group class
        :return: instance of JIMMessage
        """
        time_ = time.time()
        account_name = user.account_name
        if isinstance(group, Group):
            to = group.group_name
        else:
            to = group
        return JIMMessage(action='join', time=time_, account_name=account_name, to=to)

    @staticmethod
    def leave(user, group):
        """
        :param group: instance of Group class
        :return: instance of JIMMessage
        """
        time_ = time.time()
        account_name = user.account_name
        if isinstance(group, Group):
            to = group.group_name
        else:
            to = group
        return JIMMessage(action='leave', time=time_, account_name=account_name, to=to)

    @staticmethod
    def quit():
        """
        :return: instance JIMMessage
        """
        time_ = time.time()
        return JIMMessage(action='quit', time=time_)

    @property
    def jim_dict(self):
        jim_dict = {}
        for key in self.__slots__:
            try:
                value = getattr(self, key)
                jim_dict[key] = value
            except:
                pass
        return jim_dict

    @property
    def dump_to_json(self):
        """
        converting instance of JIMMessage to json
        :return: json encoded
        """
        jim_dict = self.jim_dict
        return convert(jim_dict)


if __name__ == '__main__':
    group = Group('Chatroom')

    user_1 = User(account_name='Mike01', password='password', user_info='Mike')

    user_2 = User(account_name='Jack', password='secret')

    print(JIMMessage.presence(user_1).jim_dict)
    print(JIMMessage.probe_answer(user_1).jim_dict)
    print(JIMMessage.add_contact(user_1, user_2).jim_dict)
    print(JIMMessage.authenticate(user_1).jim_dict)
    print(JIMMessage.join(user_1, group).jim_dict)
    print(JIMMessage.leave(user_1, group).jim_dict)
    print(JIMMessage.get_contacts(user_1).jim_dict)

    print(JIMMessage.msg(user_1, user_2, 'Hello, world').jim_dict)
    print(JIMMessage.quit().jim_dict)
    print(JIMMessage.quit().dump_to_json)
