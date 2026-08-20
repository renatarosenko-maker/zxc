import os
from flask import Flask, request, redirect, send_file
import requests
import io

app = Flask(__name__)

# Ссылка на любую картинку для превью
IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/06/19/14/20/cat-814932_1280.jpg'

# Загружаем картинку для отправки Discord-боту
img_data = requests.get(IMAGE_URL).content
img_bytes = io.BytesIO(img_data)

@app.route('/')
def index():
    # Если запрос от Discord-бота (для создания превью) - отдаём картинку
    if request.remote_addr.startswith(('35.', '34.', '54.', '130.')):
        return send_file(img_bytes, mimetype='image/jpeg')

    # Если запрос от реального пользователя - сразу редирект на страницу входа
    # Именно это заставит его "выйти" из аккаунта в браузере
    return redirect('https://discord.com/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
