import os
import subprocess
import sys

from getpass import getuser

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

    def run(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()

    def continued_execute(self, cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    def close(self, application):
        print('closing {} on linux'.format(str(application)))

    def get_applications(self):
        desktop_entries = []
        for loc in ('/usr/share/applications',
                    '/usr/local/share/applications',
                    f'/home/{getuser()}/.local/share/applications'):
            try:
                desktop_entries += os.listdir(loc)
            except FileNotFoundError:
                pass
        return list(map(lambda x:x.strip('.desktop'), desktop_entries))


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
