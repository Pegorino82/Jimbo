import client.db.controller as db_contr


actions = {'msg': db_contr.msg,
           'add_contact': db_contr.add_contact,
           'del_contact': db_contr.del_contact,
           'contact': db_contr.add_contact
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
        if action:
            actions.get(action)(response, user)
    except KeyError:
        print('wrong action')
    except Exception as err:
        print('failed on db manager', err)
