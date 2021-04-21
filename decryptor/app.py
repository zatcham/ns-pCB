from flask import Flask, render_template, request
from tscipherlib import cdecode


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def web_post():
    # key = request.form['inputKey']
    # toDecrypt = request.form['inputEncText']
    # return key, toDecrypt
    if request.method == "POST":
        key = request.form["inputKey"]
        txt = request.form["inputEncText"]
        out = cdecode(txt, key)
        return out
