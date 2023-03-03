import os.path
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import settings

def get_creds(scopes):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def generate_playlist_name():
    playlist_name = ''
    print('Генерирую название плейлиста...')

    try:
        with open(settings.KEY_WORDS_FILE) as f:
            words = [line.rstrip() for line in f]
        c = 0
    except BaseException as e:
        raise BaseException('Файл с ключевыми слоавми не найден или оформлен неправильно!')

    while c < 10:
        index = random.randint(0, len(words)-1)
        if words[index] not in playlist_name:
            playlist_name += f'{words[index]} '
            c += 1

    return playlist_name
