import telebot
from bs4 import BeautifulSoup
import requests
import random
import time

# Замените 'YOUR_TOKEN' на реальный токен вашего бота
bot = telebot.TeleBot('6958777588:AAG6Ly6WbOzDpCxNhaMx_MtItAgHi0KF-Dc')

# Замените 'YOUR_CHANNEL_ID' на идентификатор вашего канала
channel_id = '-1002007866633'

# Файл для хранения отправленных треков
sent_tracks_file = 'sent_tracks.txt'

def post_audio_to_channel():
    try:
        # Загружаем уже отправленные треки из файла
        with open(sent_tracks_file, 'r') as file:
            sent_tracks = file.read().splitlines()

        # Замените 'URL' на актуальную ссылку с busic.net
        url = 'https://busic.net/music/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем список всех треков
        track_items = soup.find_all('div', {'class': 'track-itemss'})

        # Исключаем уже отправленные треки из списка
        available_tracks = [track for track in track_items if track['data-track'] not in sent_tracks]

        if not available_tracks:
            print("Все треки были уже отправлены. Попробуйте позже.")
            return

        # Выбираем случайный трек из доступных
        random_track = random.choice(available_tracks)

        # Получаем информацию о случайном треке
        track_title = random_track['data-title']
        track_artist = random_track['data-artist']
        track_url = random_track['data-track']

        # Опубликовываем в канал
        bot.send_audio(channel_id, audio=track_url, caption=f"{track_artist} - {track_title}")

        # Добавляем отправленный трек в файл
        with open(sent_tracks_file, 'a') as file:
            file.write(track_url + '\n')

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    # Постим новый трек каждый час
    while True:
        post_audio_to_channel()
        time.sleep(3600)  # Подождать 1 час перед следующим постом