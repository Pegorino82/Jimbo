import dis

from client.errors.errors import ClientVerifierError


class FieldType:

    def __init__(self, name, value, value_type, value_len):
        self.name = "_" + name
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


class MetaJIMMessage(type):
    # action = FieldType('_action', ACTIONS[1], str, 25)
    # type_ = FieldType('_type', TYPES[0], str, 25)
    # time = FieldType('_time', TIME, float, 25)
    # user = FieldType('_user', TEMPLATE['user'], dict, 5)
    # account_name = FieldType('_account_name', ACCOUNT_NAME, str, 25)
    # status = FieldType('_status', STATUS_MESSAGE, str, 25)
    # to = FieldType('_to', TARGET, str, 25)
    # from_ = FieldType('_from', ACCOUNT_NAME, str, 25)
    # message = FieldType('_message', DEFAULT_TEXT, str, 500)
    # encoding = FieldType('_encoding', CODING, str, 15)
    #
    # slots = {action.name, type_.name, time.name, user.name, account_name.name, status.name, to.name, from_.name,
    #          message.name, encoding.name}
    slots = {'status', 'encoding', 'action', 'time', 'user', 'message', 'account_name', 'to', 'type', 'from'}

    def __new__(cls, clsname, bases, clsdict):
        clsdict['__slots__'] = cls.slots
        return type.__new__(cls, clsname, bases, clsdict)


INVALID_CALLS = {'accept', 'bind', 'listen'}


class ClientVerifier(type):

    def __new__(cls, clsname, bases, clsdict):
        for method in clsdict:
            if callable(clsdict.get(method)):
                for instr in dis.get_instructions(clsdict.get(method)):
                    if instr.argval in INVALID_CALLS:
                        raise ClientVerifierError
        return type.__new__(cls, clsname, bases, clsdict)


if __name__ == '__main__':
    name_val = FieldType('name', 'Author', str, 10)
    print(type(FieldType))
    print(isinstance(name_val, FieldType))
