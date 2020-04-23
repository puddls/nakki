import sys

from systemctl.linux_controller import LinuxController
from systemctl.mac_controller import MacController
from systemctl.windows_controller import WindowsController

def make_controller():
    if sys.platform == 'linux':
        return LinuxController()
    if sys.platform == 'darwin':
        return MacController()
    return WindowsController()

systemController = make_controller()
