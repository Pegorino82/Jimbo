import time

from ..utils.common import *
from ..utils.utils import convert
from ..base.descriptors import MetaJIMResponse, FieldType


class JIMResponse(metaclass=MetaJIMResponse):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def get_contacts(code):
        alert = CODES[code]
        return JIMResponse(action='get_contacts', response=code, quantity=0, alert=alert)

    @staticmethod
    def add_contact(contact, code):
        return JIMResponse(action='add_contact', contact=contact, response=code)

    @staticmethod
    def contacts(contact):
        return JIMResponse(action='contact', contact=contact)

    @staticmethod
    def del_contact(contact, code):
        return JIMResponse(action='del_contact', contact=contact, response=code)

    @staticmethod
    def make_response(code):
        time_ = time.time()
        if code in CODES and code < 400:
            alert = CODES[code]
            return JIMResponse(action='response', response=code, alert=alert, time=time_)
        elif code in CODES and code >= 400:
            error = CODES[code]
            return JIMResponse(action='response', response=code, error=error, time=time_)
        else:
            print('Wrong code!')

    @staticmethod
    def probe_response():
        time_ = time.time()
        return JIMResponse(action='probe', time=time_)

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

    @property
    def dump_to_json(self):
        jim_dict = self.jim_dict
        return convert(jim_dict)


if __name__ == '__main__':
    print(JIMResponse.make_response(400).dump_to_json)
    print(JIMResponse.probe_response().jim_dict)

    print(JIMResponse.__mro__)

    m = JIMResponse()
    print(m.__slots__)

    print(isinstance(JIMResponse.probe_response(), JIMResponse))

    print(JIMResponse.make_response(200).alert)
    print(JIMResponse.del_contact(123, 200).jim_dict)
