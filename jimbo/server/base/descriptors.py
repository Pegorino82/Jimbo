import dis
from ..errors.errors import ServerVerifierError
from ..utils.common import *


class FieldType:

    def __init__(self, name, value, value_type, value_len):
        self.name = name[1:]
        # self.name = "_" + name
        self.value = value
        self.value_type = value_type
        self.value_len = value_len

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.value)

    def __set__(self, instance, value):
        if not isinstance(value, self.value_type):
            raise TypeError('Value must be {}'.format(self.value_type))
        if isinstance(value, (int, float)):
            length = len(str(value))
        else:
            length = len(value)
        if length > self.value_len:
            raise ValueError('Max length must be {} symbols'.format(self.value_len))
        setattr(instance, self.name, value)


# here i have some troubles with descriptor, it doesn't work)
class MetaJIMResponse(type):
    _response = FieldType('_response', 200, int, 3)
    _alert = FieldType('_alert', DEFAULT_ALERT, str, 25)
    _error = FieldType('_error', DEFAULT_ERROR, str, 25)
    _contact = FieldType('_contact', 'Contact_default', str, 25)
    _encoding = FieldType('_encoding', CODING, str, 10)
    _action = FieldType('_action', ACTIONS[0], str, 15)
    _time = FieldType('_time', TIME, float, 25)
    _quantity = FieldType('_quantity', 5, int, 3)

    # slots = {'action', 'response', 'quantity', 'alert', 'error', 'contact', 'time', 'encoding'}
    slots = {_response.name, _alert.name, _error.name, _contact.name, _encoding.name, _action.name, _time.name, _quantity.name}

    def __new__(cls, clsname, bases, clsdict):
        clsdict['__slots__'] = cls.slots
        return type.__new__(cls, clsname, bases, clsdict)


INVALID_CALLS = {'connect'}


class ServerVerifier(type):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __new__(cls, clsname, bases, clsdict):
        for method in clsdict:
            if callable(clsdict.get(method)):
                for instr in dis.get_instructions(clsdict.get(method)):
                    if instr.argval in INVALID_CALLS:
                        raise ServerVerifierError

        return type.__new__(cls, clsname, bases, clsdict)


if __name__ == '__main__':
    name_val = FieldType('name', 'Author', str, 10)
    print(type(FieldType))
    print(isinstance(name_val, FieldType))


    class JIMResponse(metaclass=MetaJIMResponse):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        @staticmethod
        def get_contacts(code):
            alert = CODES[code]
            return JIMResponse(action='get_contacts', response=code, quantity=0, alert=alert)

        @property
        def jim_dict(self):
            show_dict = {}
            for key in self.__slots__:
                try:
                    val = getattr(self, key)
                    show_dict[key] = val
                except:
                    pass
            return show_dict


    m = JIMResponse.get_contacts(200)
    print(m.__slots__)
    print(m.jim_dict)
    m.response = 'ggg'
    print(m.response)
