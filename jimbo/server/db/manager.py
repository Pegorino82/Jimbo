from .controller import *
from .utils.utils import convert

actions = {'msg': msg,
           'presence': add_client,
           'authenticate': add_client,
           'add_contact': add_contact,
           'get_contacts': get_contacts,
           'del_contact': del_contact
           }


def manager(byte_request):
    try:
        request = convert(byte_request)
        action = request.get('action')
        return actions.get(action)(request)
    except Exception as err:
        print('failed on db manager', err)
