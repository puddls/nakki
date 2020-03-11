import sys

# TODO: use ABCMeta to make this an interface for the other controllers?
class SystemController:
    def __new__(cls):
        if sys.platform == 'linux':
            return LinuxController()
        if sys.platform == 'darwin':
            return MacController()
        return WindowsController()


class LinuxController:
    def __init__(self):
        print('linux')

    def close(self, application):
        print('closing {} on linux'.format(str(application)))


class MacController:
    def __init__(self):
        print('mac')

    def close(self, application):
        print('closing {} on mac'.format(str(application)))


class WindowsController:
    def __init__(self):
        print('windows')

    def close(self, application):
        print('closing {} on windows'.format(str(application)))
