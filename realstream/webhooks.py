from twitchAPI import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchAPI.webhook import TwitchWebHook
from pprint import pprint
from callbacks import callback_ban_changed, callback_mod_changed
from twitch_app import authenticate
from auth_scopes import authScopes

def get_user_id(username, api):
    """Returns a user ID

    Args:
        username (str): a twitch username

    Returns:
        str: a twitch user id
    """
    user_info = api.get_users(logins=[username])
    return user_info['data'][0]['id']


def main():
    # get app token
    twitch = authenticate()
    
    # get user id
    userID = get_user_id(input('Enter your twitch username: '), twitch)

    # get OAuth user token
    # for refreshing user tokens, look here: https://github.com/Teekeks/pyTwitchAPI#user-authentication
    auth = UserAuthenticator(twitch, authScopes)

    token, refresh_token = auth.authenticate()  # this will open a webpage
    twitch.set_user_authentication(token, authScopes)  # set the user authentication so any api call will also use it

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