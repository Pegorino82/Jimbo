from server.base.jimresponse import JIMResponse
from server.db.dbstorage import DBStorage
from server.db.manager import manager as db_manager
from server.db.utils.utils import convert


def get_code(request):
    byte_request = convert(request)
    code = db_manager(byte_request)
    print('from get_code:', code)
    return code


def msg(request):
    code_ = get_code(request)
    result = list()
    result.append(request)
    return result


def presence(request, code=None):
    code_ = get_code(request)
    if isinstance(code_, int):
        code = code_
    result = list()
    result.append(JIMResponse.make_response(code).jim_dict)
    return result


def auth(request, code=None):
    code_ = get_code(request)
    if isinstance(code_, int):
        code = code_
        # if code == 402
    result = list()
    result.append(JIMResponse.make_response(code).jim_dict)
    return result


def get(request, code=200):
    result = list()
    client = DBStorage(request).find_client(request.get('account_name'))
    print('client-->', client.account_name)
    contacts_list = DBStorage(request).get_contacts()
    print('contacts_list-->', contacts_list)
    res = JIMResponse.get_contacts(code).jim_dict
    res['quantity'] = len(contacts_list)
    result.append(res)
    for cont in contacts_list:
        result.append(JIMResponse.contacts(cont).jim_dict)
    print('result response->', result)
    return result


def add(request, code=None):
    code_ = get_code(request)
    if isinstance(code_, int):
        code = code_
    result = list()
    contact = request['to']
    result.append(JIMResponse.add_contact(contact, code).jim_dict)
    return result


def del_cont(request, code=None):
    code_ = get_code(request)
    if isinstance(code_, int):
        code = code_
    result = list()
    contact = request['to']
    result.append(JIMResponse.del_contact(contact, code).jim_dict)
    return result


def join():
    pass


def leave():
    pass


def quit():
    pass
