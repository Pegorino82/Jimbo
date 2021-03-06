HOST = '127.0.0.1'
PORT = 7777
SIZE = 1024
CODING = 'utf-8'
TIME = 1000000.00

PATTERN = r'({[а-яА-ЯёЁa-zA-Z0-9_\-\"\'.,:\s#?)(%$@*!№;^&+=/*|~`<>]*({[а-яА-ЯёЁa-zA-Z0-9_\-\"\'.,:\s#?)(%$@*!№;^&+=/*|~`<>]*})*[а-яА-ЯёЁa-zA-Z0-9_\-\"\'.,:\s#?)(%$@*!№;^&+=/*|~`<>]*})'

ACTIONS = ['presence',
           'authenticate',
           'join',
           'leave',
           'quit',
           'msg',
           'get_contacts',
           'add_contact',
           'del_contact',
           'response',
           'probe']
TYPES = ['text', 'img', 'video', 'audio', 'doc', 'status']

# jimmessage
USERNAME = 'Username'
TARGET = '#test_chat_room'
ACCOUNT_NAME = 'address@mail.com'
PASSWORD = None
DEFAULT_TEXT = 'default text'
STATUS_MESSAGE = 'I am here!'

# jimresponse
CODES = {100: 'Base', 101: 'Important', 200: 'OK', 201: 'Created',
         202: 'Confirmed', 400: 'Wrong request', 401: 'Not authorized',
         402: 'Wrong login/password', 403: 'User banned',
         404: 'Not founded', 409: 'Almost exists',
         410: 'Offline', 500: 'Server error'}

DEFAULT_ALERT = ''  # optional message
DEFAULT_ERROR = 'Error message'
