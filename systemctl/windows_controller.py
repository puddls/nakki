class WindowsController:
    def __init__(self):
        print('windows')

    def close(self, application):
        print(f'closing {application} on windows')

    def get_applications(self):
        return {('Discord', 'discord'), ('Spotify', 'spotify')}
