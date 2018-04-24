class ServerVerifierError(BaseException):

    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)

    def __repr__(self):
        return 'unacceptable method <connect> for socket object'

    def __str__(self):
        return 'unacceptable method <connect> for socket object'