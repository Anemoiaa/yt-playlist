from googleapiclient.discovery import build


class Youtube:
    def __init__(self, creds):
        self.service = build('youtube', 'v3', credentials=creds)

    def create_playlist(self, title, description=None, privacy_status='public'):
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
            },
            'status': {
                'privacyStatus': privacy_status,
            }
        }

        response = self.service.playlists().insert(
            part='snippet,status',
            body=request_body
        ).execute()
        return response
