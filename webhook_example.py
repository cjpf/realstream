from twitchAPI import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchAPI.webhook import TwitchWebHook
from pprint import pprint
import time

def callback_stream_changed(uuid, data):
    print('Callback Stream changed for UUID ' + str(uuid))
    pprint(data)


def callback_user_changed(uuid, data):
    print('Callback User changed for UUID ' + str(uuid))
    pprint(data)


def callback_ban_changed(uuid, data):
    print('Callback Ban changed for UUID ' + str(uuid))
    pprint(data)
    
    
def callback_mod_changed(uuid, data):
    print('Callback Mod changed for UUID ' + str(uuid))
    pprint(data)
    

clientID = '82q4j9gu5ix9edk6ig1w5215aspf0c'
cjpfID = '132493495'
#cjpfID = '582295544' #luzzyfunkins0

# basic twitch API authentication, this will yield a app token but not a user token
twitch = Twitch(clientID, 'jk4f0zbdzf8h8kogyjkqw9llp2lzap')
twitch.authenticate_app([])

# since we want user information, we require a OAuth token, lets get one
# you dont need to generate a fresh user token every time, you can also refresh a old one or get one using a different online service
# for refreshing look here: https://github.com/Teekeks/pyTwitchAPI#user-authentication
# please note that you have to add http://localhost:17563 as a OAuth redirect URL for your app, see the above link for more information
scopeList = [AuthScope.USER_READ_EMAIL, AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.MODERATION_READ, AuthScope.CHAT_READ]
auth = UserAuthenticator(twitch, scopeList)
token, refresh_token = auth.authenticate()  # this will open a webpage
twitch.set_user_authentication(token, scopeList)  # setting the user authentication so any api call will also use it

# setting up the Webhook itself
hook = TwitchWebHook("https://charliejuliet.us", clientID, 8080)
hook.authenticate(token)  # if you dont require user authentication you can also pass the app token with this: twitch.get_app_token()
# some hooks don't require any authentication, which would remove the requirement to set up a https reverse proxy
# if you don't require authentication just dont call authenticate()
hook.start()

# the hook has to run before you subscribe to any events since the twitch api will do a handshake this this webhook as soon as you subscribe
#success, uuid_stream = hook.subscribe_stream_changed(cjpfID, callback_stream_changed)
#print(f'was subscription successful?: {success}')
#success, uuid_user = hook.subscribe_user_changed(cjpfID, callback_user_changed)
#print(f'was subscription successful?: {success}')
success, uuid_ban = hook.subscribe_channel_ban_change_events(cjpfID, None, callback_ban_changed)
print(f'was subscription successful?: {success}')
success, uuid_mod = hook.subscribe_moderator_change_events(cjpfID, None, callback_mod_changed)
print(f'was subscription successful?: {success}')

# now we are fully set up and listening to our webhooks, lets wait for a user input to stop again:
input('Press enter to stop...')

# unsubscribe
#success = hook.unsubscribe_user_changed(uuid_user)
#print(f'was unsubscription successful?: {success}')
#success = hook.unsubscribe_stream_changed(uuid_stream)
#print(f'was unsubscription successful?: {success}')
success = hook.unsubscribe_channel_ban_change_events(uuid_ban)
print(f'was unsubscription successful?: {success}')
success = hook.unsubscribe_moderator_change_events(uuid_mod)
print(f'was unsubscription successful?: {success}')

time.sleep(30)

hook.stop()