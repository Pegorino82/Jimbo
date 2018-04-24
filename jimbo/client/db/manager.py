from .controller import *


actions = {'msg': controller_msg,
           'add_contact': controller_add_contact,
           'del_contact': controller_del_contact,
           'contact': controller_add_contact
           }

def manager(response, user):
    '''

    :param response: from server
    :param user: owner of account_name
    :return:
    '''
    print('mongo_db manager response->', response)
    try:
        action = response['action']
        print('mongo_db manager action->', action)
        if action in actions:
            actions.get(action)(response, user)
    except Exception as err:
        print('failed on db manager', err)
