# __author__ "lisiyu"
# date 2023/10/25

from ..settings import Settings

my_settings = Settings()


def get_chat_url():
    return my_settings.chat_url
