import telebot
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import random
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Замените 'YOUR_TOKEN' на реальный токен вашего бота
bot = telebot.TeleBot('6958777588:AAG6Ly6WbOzDpCxNhaMx_MtItAgHi0KF-Dc')

# Замените 'YOUR_CHANNEL_ID' на идентификатор вашего канала
channel_id = '-1002007866633'

# Файл для хранения отправленных треков
sent_tracks_file = 'sent_tracks.txt'

# Flask приложение
app = Flask(__name__)

# Планировщик задач
scheduler = BackgroundScheduler()

def post_audio_to_channel():
    try:
        # Загружаем уже отправленные треки из файла
        with open(sent_tracks_file, 'r') as file:
            sent_tracks = file.read().splitlines()

        # Замените 'URL' на актуальную ссылку с busic.net
        url = 'https://busic.net/'
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

# Регистрируем задачу для постинга трека каждый час
scheduler.add_job(post_audio_to_channel, 'interval', hours=1)

# Завершаем работу планировщика при выходе
atexit.register(lambda: scheduler.shutdown())

# Вебхук для приема обновлений от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return ''

if __name__ == '__main__':
    # Запускаем Flask веб-сервер
    app.run(port=5000, debug=True)

    # Запускаем планировщик задач
    scheduler.start()
