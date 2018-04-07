class ClientVerifierError(BaseException):

    def __init__(self, *args):
        BaseException.__init__(self, *args)

    def __repr__(self):
        return 'unacceptable method for socket object'

    def __str__(self):
        return 'unacceptable method for socket object'