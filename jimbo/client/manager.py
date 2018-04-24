from .controller import *

actions = {'msg': msg,
           'auth': auth,
           'get': get,
           'add': add,
           'del': delete}


def manager(user, action):
    return actions[action](user)
