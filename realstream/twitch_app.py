from twitchAPI.twitch import Twitch


appClientID = '82q4j9gu5ix9edk6ig1w5215aspf0c'
appSecret = 'h7zjcsjcnz2na2mqblyrxwlo6vhs71'


def authenticate():
    """Authenticates with a fresh generated app token

    Returns:
        [twitchAPI.Twitch]: Twitch API Client Object
    """
    twitch = Twitch(appSecret, appSecret)
    twitch.authenticate_app([])
    return twitch
