from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
from flask import Flask, jsonify, request, render_template
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    username = request.form['username']
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    url = f'https://atcoder.jp/users/{username}'

    try:
        # Seleniumのセットアップ
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # ヘッドレスモードで実行
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # ウェブページを開く
        driver.get(url)

        # ページが完全に読み込まれるまで待機 (最大10秒), 1秒単位
        driver.implicitly_wait(10)

        # canvas要素をIDで取得
        canvas = driver.find_element_by_id('ratingGraph')

        # canvas要素のスクリーンショットを撮る
        canvas_screenshot = canvas.screenshot_as_png

        # スクリーンショットをPillowで画像として保存
        image = Image.open(io.BytesIO(canvas_screenshot))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # 現在時刻を取得
        filename = f'rating_graph_image_{username}_{timestamp}.png'
        image_path = os.path.join(app.static_folder, filename)
        image.save(image_path)

        # ブラウザを閉じる
        driver.quit()

        # 画像のURLを生成
        image_url = f'/static/{filename}'

        return jsonify({'message': f'スクリーンショットが保存されました: {filename}', 'url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()