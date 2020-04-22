from scheduler import Scheduler


class SystemController:
    def __init__(self):
        self.schedule_manager = Scheduler()
        self.schedule_manager.run_continuously()

    def open(self, application):
        print(f'open {application}')

    def close(self, application):
        print(f'close {application}')
    
    def get_applications(self):
        return {('Discord', 'discord'), ('Spotify', 'spotify')}

    def schedule_task(self, action, target, trigger):
        print(f'schedule: {action} {target} when: {trigger}')
        if trigger[0] == 'daily':
            try:
                self.schedule_manager.every(1).day \
                                     .at(trigger[1]) \
                                     .do(lambda: self.exec_task(action, target))
                return True
            except AssertionError:
                print('invalid time')
                return False
        else:
            return None

    def exec_task(self, action, target):
        if action == 'open':
            self.open(target)
        elif action == 'close':
            self.close(target)
        else:
            return None
        return True
