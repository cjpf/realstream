from twitchAPI.twitch import Twitch
from twitchAPI import UserAuthenticator
from auth_scopes import userAuthScopes


appClientID = '82q4j9gu5ix9edk6ig1w5215aspf0c'
appSecret = 'h7zjcsjcnz2na2mqblyrxwlo6vhs71'


def app_authenticate():
    """Authenticates with a fresh generated app token

    Returns:
        [twitchAPI.Twitch]: Twitch API Client Object
    """
    twitch = Twitch(appSecret, appSecret)
    twitch.authenticate_app([])
    return twitch


def user_authenticate(twitch_app):
    """Generates an OAuth token
        for refreshing user tokens, look here: https://github.com/Teekeks/pyTwitchAPI#user-authentication
    Args:
        twitch_app ([twitchAPI.Twitch]): Twitch API Client Object

    Returns:
        [type]: user access token
        [type]: refresh token
    """
    auth = UserAuthenticator(twitch_app)
    token, refresh_token = auth.authenticate() # this will open a webpage
    # set the user authentication so any api call will also use it
    twitch_app.set_user_authentication(token, userAuthScopes)
    return token, refresh_token
