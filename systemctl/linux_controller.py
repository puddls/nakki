import os
import subprocess
import re
from threading import Thread

from getpass import getuser

from systemctl.system_controller import SystemController

class LinuxController(SystemController):
    def __init__(self):
        super().__init__()
        print('linux')

    def open(self, application):
        launch(application)

    def close(self, application):
        # TODO: this requires it to match the process name, but that might not be the command to launch
        # (e.g. google-chrome-stable vs chrome, discord vs Discord, etc)
        # maybe use get_user_ps somehow? ask the user to open the app and then select it from that list?
        run(f'pkill {application}')

    def get_actions(self):
        return super().get_actions().union({('Custom command','command')})
    
    def get_triggers(self):
        return super().get_triggers().union({('Removable drive', 'rem_drive')})

    def get_user_ps(self):
        ''' Finds processes owned by the user that aren't obviously system processes.
        Returns a set of process names. '''
        ps = run(f'ps -eu {getuser()}')[0].decode().split('\n')
        ps_names = set((p.strip().split(' ')[-1] for p in ps))
        likely_ps = set((p for p in ps_names if '/' not in p))
        return likely_ps

    def get_applications(self):
        ''' Finds installed applications (specifically those with a .desktop file,
        the same set that would be found by a start menu)
        Returns a set of tuples: {(application name, command to execute), ...} '''
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
            if trigger[0] == 'rem_drive':
                Thread(target=lambda: self.udisk_monitor(action, target, trigger[1])).start()
        return False

    def exec_task(self, action, target):
        spr = super().exec_task(action, target)
        if spr is None:
            if action == 'command':
                run(target)
                return True
        return False

    def udisk_monitor(self, action, target, trigger):
        # TODO: integrate with other stuff so there can't ever be multiple of these running
        change = False
        for line in continued_execute('udisksctl monitor'):
            if change:
                if 'Drive' in line:
                    Thread(target=lambda: self.exec_task(action, target)).start()
                change = False
            if trigger == 'inserted' and 'Added' in line:
                change = True
            if trigger == 'removed' and 'Removed /org/freedesktop/UDisks2/drives' in line:
                Thread(target=lambda: self.exec_task(action, target)).start()


def launch(application):
    os.system(application)


def run(command):
    ''' Runs the command as though it were typed into a bash prompt
    Returns a tuple of (stdout, stderr) in bytes '''
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def continued_execute(cmd):
    ''' Used for commands that numerous lines of output over time (e.g. 'udiskctl monitor')
    Should be iterated through in a thread, it will yield each line of output when it gets it from stdout '''
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def parse_desktop_entry(file):
    ''' Goes from a .desktop file to the usefull application info
    Returns a tuple (application name, command to execute) '''
    if '.desktop' not in file:
        return None
    f = open(file).read()
    # Ignore junk at the top
    start = re.search(r'\[Desktop Entry\]', f)
    if start:
        # Find the end of the desktop entry (there could be other stuff, also marked by [name] ...)
        s = start.span()[1]
        end = re.search(r'\n\[.*\]', f[s:])
        if end:
            e = end.span()[0]
        else:
            e = None
        entry = f[s:e]
        name = None
        exec_ = None
        # Find the name and exec, and make sure its actually an application
        for line in entry.split('\n'):
            if 'Name=' in line:
                name = line.split('=')[1]
            elif 'Exec=' in line:
                exec_ = line.split('=')[1]
            elif 'Type=' in line:
                if not 'Application' in line:
                    return None
        return (name, exec_)
