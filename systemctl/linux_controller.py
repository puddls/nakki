import os
import subprocess
import re

from getpass import getuser

from systemctl.system_controller import SystemController

class LinuxController(SystemController):
    def __init__(self):
        super().__init__()
        print('linux')

    def open(self, application):
        launch(application[1])

    def close(self, application):
        # TODO: this requires it to match the process name, but that might not be the command to launch
        # (e.g. google-chrome-stable vs chrome, discord vs Discord, etc)
        # maybe use get_user_ps somehow? ask the user to open the app and then select it from that list?
        run(f'pkill {application[1]}')

    def get_user_ps(self):
        ps = run(f'ps -eu {getuser()}')[0].decode().split('\n')
        ps_names = set((p.strip().split(' ')[-1] for p in ps))
        likely_ps = set((p for p in ps_names if '/' not in p))
        return likely_ps

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

    def schedule_task(self, action, target, trigger):
        # Try the generic, platform independent triggers
        spr = super().schedule_task(action, target, trigger)
        # If it wasn't one of those, try platform dependant triggers
        if spr is None:
            pass
            # if trigger[0] == 'some trigger that only works on linux':
            #     schedule task with this trigger
        return False

    def exec_task(self, action, target):
        spr = super().exec_task(action, target)
        if spr is None:
            pass
            # if action == 'some action that only works on linux':
            #     execute action
        return False


def launch(application):
    os.system(application)


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
