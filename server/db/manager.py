import server.db.controller as db_contr
from server.db.utils.utils import convert

actions = {'msg': db_contr.msg,
           'presence': db_contr.add_client,
           'authenticate': db_contr.add_client,
           'add_contact': db_contr.add_contact,
           'get_contacts': db_contr.get_contacts,
           'del_contact': db_contr.del_contact
           }


def manager(byte_request):
    try:
        request = convert(byte_request)
        action = request.get('action')
        return actions.get(action)(request)
    except Exception as err:
        print('failed on db manager', err)
