from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hemlo World"

@app.route("/harry")
def harry():
    return "Hemlo Harry bhai! Bullaa"

app.run(debug=True)