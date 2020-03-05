import sys

from systemctl.linux_controller import LinuxController
from systemctl.mac_controller import MacController
from systemctl.windows_controller import WindowsController

# TODO: use ABCMeta to make this an interface for the other controllers?
class SystemController:
    def __new__(cls):
        return LinuxController() if sys.platform=='linux' else MacController() if sys.platform=='darwin' else WindowsController()
