from flask import Flask, request, render_template
from selenium import webdriver

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = str(request.form['username'])
        url = "https://atcoder.jp/users/" + username
        driver = webdriver.Chrome()
        driver.get(url)
        canvas_element = driver.find_element(By.ID,'ratingGraph')
        # Canvas 要素を data URI 化して取得
        canvas_data_url = driver.execute_script("return arguments[0].toDataURL('');", canvas_element)
        # SVG化
        #svg = driver.execute_script("return arguments[0].toSVG();", canvas_element)
        # テンプレートに載せて表示
        return render_template('index.html', canvas_data_url=canvas_data_url)
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)