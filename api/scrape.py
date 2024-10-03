from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
from flask import Flask, jsonify, request
from datatime import datetime
import os
##import pyperclip

#Flaskのセットアップ
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#/api/scrapeエンドポイントのGETリクエストを処理
@app.route('/scrape', methods=['POST'])
def scrape(): #スクレイピング処理
    username = request.form['username'] #usernameを取得
    if not username: #usernameが指定されていない場合
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

        # canvas要素を取得
        canvas = driver.find_element_by_tag_name(ratingGraph)

        # canvas要素のスクリーンショットを撮る
        canvas_screenshot = canvas.screenshot_as_png

        # スクリーンショットをPillowで画像として保存
        image = Image.open(io.BytesIO(canvas_screenshot))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # 現在時刻を取得
        filename = f'rating_graph_image_{username}_{timestamp}.png'
        image_path = os.path.join('/tmp', filename)
        image.save(image_path)

        # ブラウザを閉じる
        driver.quit()

        # 画像のURLを生成
        image_url = f'/tmp/{filename}'

        return jsonify({'message': f'スクリーンショットが保存されました: {filename}', 'url': image_url})
        #スクレイピング結果URLをクリップボードにコピーする


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()