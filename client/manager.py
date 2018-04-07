import client.controller as client_contr

actions = {'msg': client_contr.msg,
           'auth': client_contr.auth,
           'get': client_contr.get,
           'add': client_contr.add,
           'del': client_contr.delete}


def manager(user, action):
    return actions[action](user)
