from twitchAPI.types import AuthScope
from twitchAPI.webhook import TwitchWebHook
from pprint import pprint
from callbacks import callback_ban_changed, callback_mod_changed
from twitch_app import app_authenticate, user_authenticate

def get_user_id(username, twitch):
    """Returns a user ID

    Args:
        username (str): a twitch username
        twitch (twitchAPI.Twitch): an authenticated Twitch API Client Object

    Returns:
        str: a twitch user id
    """
    user_info = twitch.get_users(logins=[username])
    return user_info['data'][0]['id']


def main():
    # get app token
    twitch = app_authenticate()
    
    # get user id
    userID = get_user_id(input('Enter your twitch username: '), twitch)

    # get OAuth user token
    token, refresh_token = user_authenticate(twitch)

    # set up the Webhook 
    hook = TwitchWebHook("https://charliejuliet.us", appClientID, 8080)
    hook.authenticate(token) 

    # the hook has to run before you subscribe to any events since the twitch api will do a handshake this this webhook as soon as you subscribe
    hook.start()


    success, uuid_ban = hook.subscribe_channel_ban_change_events(userID, None, callback_ban_changed)
    print(f'was subscription successful?: {success}')
    success, uuid_mod = hook.subscribe_moderator_change_events(userID, None, callback_mod_changed)
    print(f'was subscription successful?: {success}')

    # wait for a user input to unsubscribe
    input('Press enter to stop...')

    # unsubscribe
    success = hook.unsubscribe_channel_ban_change_events(uuid_ban)
    print(f'was unsubscription successful?: {success}')
    success = hook.unsubscribe_moderator_change_events(uuid_mod)
    print(f'was unsubscription successful?: {success}')

    hook.stop()


if __name__ == "__main__":
    main()