from scheduler import Scheduler


class SystemController:
    def __init__(self):
        self.schedule_manager = Scheduler()
        self.cease_continuous_run = self.schedule_manager.run_continuously()

    def pause_all_tasks(self):
        self.cease_continuous_run.set()

    def resume_all_tasks(self):
        self.cease_continuous_run = self.schedule_manager.run_continuously()

    def clear_tasks(self):
        self.schedule_manager.clear()

    def open(self, application):
        print(f'open {application}')

    def close(self, application):
        print(f'close {application}')

    def get_actions(self):
        return {('Open', 'open'), ('Close', 'close')}
    
    def get_triggers(self):
        return {('Daily', 'daily'), ('Periodic (minutes)', 'periodic_min')}

    def get_applications(self):
        ''' Return a list of installed applications as a set of tuples
        in the format: {(application name, command to execute)}'''
        return {('Discord', 'discord'), ('Spotify', 'spotify')}

    def schedule_task(self, action, target, trigger):
        ''' Schedules a task
        action: what is being done, e.g. 'open' or 'close'.
            Avalible actions types can be found in exec_task, additional options
            may be avalible in the OS specific implementation
        target: thing to action on, in the format (human friendly name, computer friendly name)
            Example: ('Chrome Browser', 'google-chrome-stable')
        trigger: tuple specifying when to execute, in the form (type, value).
            Example: ('daily', '14:30') will run every day at 2:30 PM.
            Avalible trigger types can be found in this function, more may be
            avalible in the OS specific implementation.
        Returns True for success, False for failure, None for an invalid trigger '''
        print(f'scheduling: {action} {target} when: {trigger}')
        if trigger[0] == 'daily':
            # Every day
            try:
                # Time should be in the format HH:MM, using a 24 hour clock
                self.schedule_manager.every(1).day \
                                     .at(trigger[1]) \
                                     .do(lambda: self.exec_task(action, target))
                return True
            except AssertionError:
                print('invalid time')
                return False
        elif trigger[0] == 'periodic_min':
            # Every n minutes
            try:
                frequency = int(trigger[1])
                self.schedule_manager.every(frequency).minutes \
                                     .do(lambda: self.exec_task(action, target))
                return True
            except ValueError:
                print('invalid time')
                return False
        else:
            return None

    def exec_task(self, action, target):
        print(f'executing {action} on {target}')
        if action == 'open':
            self.open(target)
        elif action == 'close':
            self.close(target)
        else:
            return None
        return True
