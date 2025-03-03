from gpiozero import MotionSensor
from signal import pause
import requests
from picamera import PiCamera
from time import sleep
import os

# Настройки для Telegram
TOKEN = '7010897855:AAEH5EPyYjn9HE7s9bC1uAjC6wSVnzHOnLk'
CHAT_ID = '2190977460'  # Замените на chat_id вашей группы

# Инициализация PIR-датчика
pir = MotionSensor(18)

# Инициализация камеры
camera = PiCamera()
camera.resolution = (1024, 768)  # Установите разрешение фото
PHOTO_PATH = '/tmp/photo.jpg'  # Временный путь для сохранения фото

# Функция для отправки фото в Telegram
def send_photo_to_telegram():
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    with open(PHOTO_PATH, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        print("Фото успешно отправлено в Telegram!")
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.json())

# Функция для создания фото
def take_photo():
    print("Делаю фото...")
    camera.capture(PHOTO_PATH)  # Делаем фото и сохраняем его
    print(f"Фото сохранено: {PHOTO_PATH}")

# Функция, вызываемая при обнаружении движения
def motion_function():
    print("Движение обнаружено!")
    take_photo()  # Делаем фото
    send_photo_to_telegram()  # Отправляем фото в Telegram

# Функция, вызываемая при отсутствии движения
def no_motion_function():
    print("Движение прекратилось")

# Назначаем функции обработчиками событий
pir.when_motion = motion_function
pir.when_no_motion = no_motion_function

# Оставляем программу активной
pause()