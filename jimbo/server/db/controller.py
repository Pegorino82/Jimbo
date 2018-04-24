from ..project_path import PROJECT_PATH
import sys

sys.path.insert(0, PROJECT_PATH)

from .dbstorage import DBStorage


def add_client(request):
    action = request.get('action')
    account_name = DBStorage(request).get_user['account_name']
    password = DBStorage(request).get_user['password']
    client = DBStorage(request).find_client(account_name)
    if action == 'authenticate':
        if not client:
            code = DBStorage(request).add_client()
            DBStorage(request).add_to_history()
            return code
        else:
            if client.password == password:
                DBStorage(request).add_to_history()
                return 200
            else:
                return 402
    elif action == 'presence':
        if client:
            return 200
        else:
            return 404


def add_contact(request):
    code = DBStorage(request).add_contact()
    DBStorage(request).add_to_history()
    return code


def del_contact(request):
    code = DBStorage(request).del_contact()
    DBStorage(request).add_to_history()
    return code


def get_contacts(request):
    DBStorage(request).get_contacts()
    DBStorage(request).add_to_history()


def msg(request):
    DBStorage(request).add_message()
    DBStorage(request).add_to_history()


if __name__ == '__main__':
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
    #
    # write_to_db(cli_1)
    # write_to_db(cli_2)
    # write_to_db(cli_3)
    # write_to_db(cli_4)
    #
    # write_to_db(add_1)
    # write_to_db(add_2)
