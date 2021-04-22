from flask import Flask, render_template, request, jsonify
from tscipherlib import cdecode
from nsCB_decrypt import tsDecrypt

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

        out = tsDecrypt(txt, key)
        return render_template("result.html", out=out)

if __name__ == "__main__":
   app.run(debug = True)
