from client.base.jimmessage import JIMMessage


def auth(user):
    byte_request = JIMMessage.authenticate(user).dump_to_json
    return byte_request


def add(user):
    to = input('type contact account_name:')
    byte_request = JIMMessage.add_contact(user, to).dump_to_json
    return byte_request


def get(user):
    byte_request = JIMMessage.get_contacts(user).dump_to_json
    return byte_request


def delete(user):
    to = input('type contact account_name:')
    byte_request = JIMMessage.del_contact(user, to).dump_to_json
    return byte_request

def msg(user):
    # target = '#' + input(
    #     'enter target (type anything, in all cases it is for all:)): ')
    message = input('type text (<exit> for exit): ')
    if message == 'exit':
        return
    byte_request = JIMMessage.msg(user, message, to='#chat').dump_to_json
    print('prepared message', byte_request)
    return byte_request
