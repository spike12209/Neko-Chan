from functions import logger, config
import asyncio

class Music:
    def __init__(self, user, type, url, title=""):
        ''' Initialize the Music object '''
        if isinstance(user, str):
            self.user = user
        else:
            self.user = user.display_name
        self.title = title
        self.type = type
        self.url = url