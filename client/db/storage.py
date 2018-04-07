from pymongo import MongoClient


CLIENT_DB = '_client_db'
client = MongoClient()
client_db = client[CLIENT_DB]

contacts = client_db.contacts
in_messages = client_db.income_messages
out_messages = client_db.outcome_messages


class Contact:
    __slots__ = {'name', 'user_info'}

    def __init__(self, name):
        self.name = name

    @property
    def con_dict(self):
        con_d = dict()
        for key in self.__slots__:
            if hasattr(self, key):
                con_d.update({key: getattr(self, key)})
        return con_d


def add_contact(contact):
    for cont in client_db.contacts.find():
        if cont['name'] == contact['name']:
            return 'almost in contacts'
    client_db.contacts.insert_one(contact)
    return '{} added'.format(contact['name'])


def del_contact(contact):
    for cont in client_db.contacts.find():
        if cont['name'] == contact['name']:
            client_db.contacts.delete_one(contact)
            return '{} deleted'.format(contact['name'])
    return '{} not found'.format(contact['name'])


def add_message(user, message):
    if message['account_name'] == user:
        client_db.outcome_messages.insert_one(message)
        return 'message to {} added'.format(message['to'])
    else:
        client_db.income_messages.insert_one(message)
        return 'message from {} added'.format(message['account_name'])


if __name__ == '__main__':
    cont_1 = Contact('Jack').con_dict
    cont_2 = Contact('Bob').con_dict
    cont_3 = Contact('Trent').con_dict

    print('1*', client_db)
    # client_db.name = 'New_name'
    print('1**', client_db.name)
    print('2*', client_db.contacts.find({'name': 'Jack'}))

    for cont in client_db.contacts.find():
        print(cont)


    def add_income_message(message):
        pass


    print(add_contact(cont_1))
    print(add_contact(cont_2))
    print(add_contact(cont_3))
    cont_4 = {'name': 'Hugh'}
    print(add_contact(cont_4))

    print(del_contact(cont_2))

    for cont in client_db.contacts.find():
        print(cont)

    # client.drop_database(client_db)

    cl = Contact('Fred')
    cl.user_info = 'info'
    print(cl.con_dict)

    messag = {'action': 'msg', 'encoding': 'utf-8', 'time': 1522332913.4264934, 'account_name': 'Mary',
              'message': 'fghfgh',
              'to': '#'}

    add_message('Trent', messag)

    for mess in client_db.outcome_messages.find():
        print('out', mess)

    for mess in client_db.income_messages.find():
        print('in', mess)
