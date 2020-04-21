class SystemController:
    def open(self, application):
        print(f'open {application}')

    def close(self, application):
        print(f'close {application}')
    
    def get_applications(self):
        return {('Discord', 'discord'), ('Spotify', 'spotify')}

    def schedule_task(self, action, target, trigger):
        print(f'schedule: {action} {target} when: {trigger}')
        print('scheduling not implemented, executing now')
        self.exec_task(action, target)

    def exec_task(self, action, target):
        if action == 'open':
            self.open(target)
        elif action == 'close':
            self.close(target)
        else:
            return False
