import server.controller as serv_contr
from server.utils.utils import convert

actions = {'msg': serv_contr.msg,
           'presence': serv_contr.presence,
           'authenticate': serv_contr.auth,
           'get_contacts': serv_contr.get,
           'add_contact': serv_contr.add,
           'del_contact': serv_contr.del_cont,
           'join': serv_contr.join,
           'leave': serv_contr.leave,
           'quit': serv_contr.quit}


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
