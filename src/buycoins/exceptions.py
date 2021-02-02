class _BaseException(Exception):
    pass


class NoConnectionError(_BaseException):
    def __init__(self):
        super().__init__("No active connection: have you initialized yet?")


class ExecutionError(_BaseException):
    pass


class RemoteServerError(_BaseException):
    pass
