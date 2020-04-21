from systemctl.system_controller import SystemController


class WindowsController(SystemController):
    def __init__(self):
        print('windows')
