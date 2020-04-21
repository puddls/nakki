from systemctl.system_controller import SystemController


class MacController(SystemController):
    def __init__(self):
        print('mac')
