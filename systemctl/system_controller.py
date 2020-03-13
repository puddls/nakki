import sys

from systemctl.linux_controller import LinuxController
from systemctl.mac_controller import MacController
from systemctl.windows_controller import WindowsController

# TODO: use ABCMeta to make this an interface for the other controllers?
class SystemController:
    def __new__(cls):
        if sys.platform == 'linux':
            return LinuxController()
        if sys.platform == 'darwin':
            return MacController()
        return WindowsController()
    
    def close(self, application):
        pass

    def get_applications(self):
        pass


systemController = SystemController()
