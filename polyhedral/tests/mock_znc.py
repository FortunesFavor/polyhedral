import mock

CONTINUE = '--continue--'


class Module:
    def __init__(self):
        self.nv = dict()
        self.PutModule = mock.MagicMock()
        self.PutIRC = mock.MagicMock()
