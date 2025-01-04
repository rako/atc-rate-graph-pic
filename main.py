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
        