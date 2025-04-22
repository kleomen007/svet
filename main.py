#!/usr/bin/env python3
from gpiozero import MotionSensor
from picamera import PiCamera
import requests
from time import sleep, strftime
import os
from signal import pause

# Конфигурация
TOKEN = '7010897855:AAEH5EPyYjn9HE7s9bC1uAjC6wSVnzHOnLk'
CHAT_ID = '2190977460'
PIR_PIN = 18
PHOTO_DIR = '/var/motion_photos'  # Более подходящая директория для фото

# Создаем директорию для фото, если ее нет
os.makedirs(PHOTO_DIR, exist_ok=True)

# Инициализация устройств
pir = MotionSensor(PIR_PIN)
camera = PiCamera()
camera.resolution = (1024, 768)

def get_photo_path():
    """Генерирует уникальное имя файла с timestamp"""
    return os.path.join(PHOTO_DIR, f"motion_{strftime('%Y%m%d_%H%M%S')}.jpg")

def take_photo():
    """Делает фото и возвращает путь к файлу"""
    photo_path = get_photo_path()
    print(f"Делаю фото: {photo_path}")
    camera.capture(photo_path)
    return photo_path

def send_photo_to_telegram(photo_path, caption=""):
    """Отправляет фото в Telegram с подписью"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    try:
        with open(photo_path, 'rb') as photo:
            response = requests.post(
                url,
                files={'photo': photo},
                data={
                    'chat_id': CHAT_ID,
                    'caption': caption or f"Движение обнаружено {strftime('%Y-%m-%d %H:%M:%S')}",
                    'parse_mode': 'HTML'
                },
                timeout=10
            )
        if response.status_code == 200:
            print("Фото успешно отправлено!")
        else:
            print(f"Ошибка Telegram API: {response.json()}")
    except Exception as e:
        print(f"Ошибка при отправке фото: {str(e)}")

def motion_detected():
    """Обработчик движения"""
    print("Движение обнаружено!")
    try:
        photo_path = take_photo()
        send_photo_to_telegram(photo_path, "⚠️ Обнаружено движение! ⚠️")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def no_motion():
    """Обработчик отсутствия движения"""
    print("Движение прекратилось")

# Настройка обработчиков событий
pir.when_motion = motion_detected
pir.when_no_motion = no_motion

print("Система мониторинга движения запущена...")
pause()
