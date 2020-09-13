from twitchAPI.twitch import Twitch
from webhooks import twitch


def get_user_id(username):
    """Returns a user ID

    Args:
        username (str): a twitch username

    Returns:
        str: a twitch user id
    """
    user_info = twitch.get_users(logins=[username])
    return user_info.id
