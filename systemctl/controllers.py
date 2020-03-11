import os
import subprocess
import sys
import re

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
        desktop_entries = set()
        for loc in ('/usr/share/applications/',
                    '/usr/local/share/applications/',
                    f'/home/{getuser()}/.local/share/applications/'):
            try:
                desktop_entries.update(map(lambda x: loc + x, os.listdir(loc)))
            except FileNotFoundError:
                pass
        return set(map(self.parse_desktop_entry, desktop_entries))
    
    def parse_desktop_entry(self, file):
        if '.desktop' in file:
            f = open(file).read()
            start = re.search(r'\[Desktop Entry\]', f)
            if start:
                s = start.span()[1]
                end = re.search(r'\n\[.*\]', f[s:])
                if end:
                    e = end.span()[0]
                else:
                    e = None
                entry = f[s:e]
                name = None
                exec_ = None
                for line in entry.split('\n'):
                    if 'Name=' in line:
                        name = line.split('=')[1]
                    elif 'Exec=' in line:
                        exec_ = line.split('=')[1]
                    elif 'Type=' in line:
                        if not 'Application' in line:
                            return None
                return (name, exec_)
        return None


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
