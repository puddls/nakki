class MacController:
    def __init__(self):
        print('mac')

    def close(self, application):
        print(f'closing {application} on mac')

    def get_applications(self):
        return {('Discord', 'discord'), ('Spotify', 'spotify')}
