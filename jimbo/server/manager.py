from .controller import *
from .utils.utils import convert

actions = {'msg': msg,
           'presence': presence,
           'authenticate': auth,
           'get_contacts': get,
           'add_contact': add,
           'del_contact': del_cont,
           'join': join,
           'leave': leave,
           'quit': quit}


def manager(byte_request):
    '''
    make responses
    :param byte_request: byte request from client
    :return:list of responses
    '''
    try:
        request = convert(byte_request)
        action = request.get('action')
        print('action-->', action)
        manager_result = actions[action](request)
        # print('manager result', manager_result)
        return manager_result
    except Exception as err:
        print('error-->', err)
        return False
