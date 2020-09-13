from pprint import pprint


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
    
