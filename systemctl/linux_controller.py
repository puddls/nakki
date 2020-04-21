import os
import subprocess
import re

from getpass import getuser

from systemctl.system_controller import SystemController

class LinuxController(SystemController):
    def __init__(self):
        print('linux')

    def close(self, application):
        print(f'closing {application} on linux')

    def get_applications(self):
        desktop_entries = set()
        for loc in ('/usr/share/applications/',
                    '/usr/local/share/applications/',
                    f'/home/{getuser()}/.local/share/applications/'):
            try:
                desktop_entries.update((loc + x for x in os.listdir(loc)))
            except FileNotFoundError:
                pass
        return set(filter(None, map(parse_desktop_entry, desktop_entries)))

def run(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def continued_execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def parse_desktop_entry(file):
    if '.desktop' not in file:
        return None
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
