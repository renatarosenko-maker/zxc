import os
from flask import Flask, request, send_file, render_template_string
import requests
import io

app = Flask(__name__)

IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/06/19/14/20/cat-814932_1280.jpg'
img_data = requests.get(IMAGE_URL).content
img_bytes = io.BytesIO(img_data)

LOGOUT_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta property="og:image" content="{{ image_url }}">
    <meta property="og:title" content=" ">
    <meta property="og:description" content=" ">
    <title>Discord</title>
    <style>
        body { margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; background: #313338; font-family: Arial; }
        .container { text-align: center; color: white; }
        img { max-width: 400px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
        .status { margin-top: 20px; font-size: 16px; color: #b5bac1; }
        .spinner { width: 40px; height: 40px; border: 4px solid #5865F2; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <img src="{{ image_url }}" alt="image">
        <div class="spinner"></div>
        <div class="status">Выход из аккаунта...</div>
    </div>
    <script>
        setTimeout(function() {
            // 1. Удаляем все куки Discord
            document.cookie.split(";").forEach(function(c) {
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
            });

            // 2. Очищаем localStorage и sessionStorage
            try { localStorage.clear(); sessionStorage.clear(); } catch(e) {}

            // 3. Перенаправляем на страницу входа
            window.location.href = "https://discord.com/login";
        }, 2500);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    if request.remote_addr.startswith(('35.', '34.', '54.', '130.')):
        return send_file(img_bytes, mimetype='image/jpeg')
    return render_template_string(LOGOUT_PAGE, image_url=IMAGE_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
