from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import isodate

from youtube import Youtube
from config import settings
import utils

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]


def main():
    try:
        with open(settings.LINKS_FILE) as f:
            links = [line.rstrip() for line in f]
    except BaseException as e:
        raise BaseException("Файл с ссылками не найден или оформлен неправильно!")

    chrome_profile = webdriver.ChromeOptions()
    chrome_profile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_profile.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_profile)

    video_ids = []
    last_vide_selector = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a'

    print('Начинаю парсить последние видео с каналов...')
    for link in links:
        driver.get(f'{link}/videos')
        try:
            content = WebDriverWait(driver, settings.DELAY).until(
                EC.presence_of_element_located((By.XPATH, last_vide_selector))
            )
            href = content.get_attribute('href')
            id_start = href.find('?v=') + 3
            video_ids.append(href[id_start::])
        except TimeoutError as e:
            print(f'На канале по ссылке {link} нет видео или мы столкнулись с неизвестной ошибкой...')
    print('Закончил...')

    creds = utils.get_creds(SCOPES)

    yt = Youtube(creds)
    playlist_name = utils.generate_playlist_name()

    print(f'Создаю плейлист {playlist_name}')
    response_playlist = yt.create_playlist(playlist_name)
    playlist_id = response_playlist.get('id')
    playlist_title = response_playlist['snippet']['title']

    for video_id in video_ids:
        # get duration
        request = yt.service.videos().list(
            part="contentDetails",
            id=video_id,
        )
        response = request.execute()

        video_duration = isodate.parse_duration(response['items'][0]['contentDetails']['duration'])
        max_duration = isodate.parse_duration(settings.MAX_DURATION)
        if video_duration > max_duration:
            continue

        request_body = {
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
        response = yt.service.playlistItems().insert(
            part='snippet',
            body=request_body
        ).execute()
        video_title = response['snippet']['title']
        print(f'Видео "{video_title}" добавлено в {playlist_title} плейлист')


if __name__ == '__main__':
    main()
