import time
import os

FILE_NAME = 'storage.txt'
FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)


class Storage:

    def __init__(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def get_user(self):
        user = {'account_name': None, 'password': None, 'user_info': None}
        for key in self.__dict__:
            if key == 'user':
                user['account_name'] = self.__dict__[key]['account_name']
                user['user_info'] = 'TODO: add <user_info> for user'
                try:
                    user['password'] = self.__dict__[key]['password']
                except KeyError:
                    pass
            elif key == 'account_name':
                user['account_name'] = self.__dict__[key]
        return user

    @property
    def get_contact(self):
        contact = {'to': None}
        for key in self.__dict__:
            if key == 'to':
                contact['to'] = self.__dict__[key]
        return contact

    @property
    def get_action(self):
        action = {'action': None}
        for key in self.__dict__:
            if key == 'action':
                action['action'] = self.__dict__[key]
        return action

    @property
    def get_message(self):
        message = {'message': None}
        for key in self.__dict__:
            if key == 'message':
                message['message'] = self.__dict__[key]
        return message

    @property
    def get_to(self):
        to = {'to': None}
        for key in self.__dict__:
            if key == 'to':
                to['to'] = self.__dict__[key]
        return to


class FileStorage(Storage):

    def __init__(self, kwargs):
        super().__init__(kwargs=kwargs)
        self.file = FILE_PATH

    @property
    def get_time(self):
        time__ = {'time': None}
        time_ = time.time()
        t_local = time.localtime(time_)
        t = time.strftime('%d.%m.%Y - %H:%M:%S', t_local)
        time__['time'] = [x.strip() for x in t.split('-')]
        return time__

    @property
    def make_data(self):
        time_ = self.get_time.get('time')
        user = self.get_user.get('account_name')
        action = self.get_action.get('action')
        message = self.get_message.get('message')
        to = self.get_to.get('to')
        if message:
            return '{} {} | user: {:<10} | action: {:<10} | to: {:<10} | message: {}\n'.format(time_[0], time_[1], user,
                                                                                               action, to, message)
        else:
            return '{} {} | user: {:<10} | action: {:<10}\n'.format(time_[0], time_[1], user, action, to, message)

    def write_data(self, data):
        with open(self.file, 'a') as file:
            file.write(data)


if __name__ == '__main__':
    d = {'action': 'test', 'user': {'account_name': 'Jack', 'password': '123'}}
    dd = {'action': 'msg', 'to': '#chat', 'message': 'testtext', 'time': 1520535974.6585314, 'account_name': 'Jack'}
    ad = {'to': 'User_3', 'action': 'add_contact', 'account_name': 'User_1', 'time': 1521555431.914513}

    sad = Storage(ad)
    print(sad.get_action)
    print(sad.get_user)
    print(sad.get_time)
    print(sad.get_message)
    print(sad.get_contact)

    s = Storage(d)
    print(s.get_action)
    print(s.get_user)
    print(s.get_time)
    print(s.get_message)

    f = FileStorage(d)
    data = f.make_data
    f.write_data(data)

    ff = FileStorage(dd)
    data = ff.make_data
    ff.write_data(data)
