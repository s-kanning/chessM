import API_config
import berserk

def user_lookup(username):
    session = berserk.TokenSession(API_config.api_key)
    client = berserk.Client(session=session)
    info = client.users.get_by_id(username)
    game_data = ['bullet', 'blitz', 'rapid']
    cleaned_data = []
    for item in game_data:
        cleaned_data.append(info[0]['perfs'][item]['rating'])
    return cleaned_data



