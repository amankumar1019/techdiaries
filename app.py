from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

with open('config.json') as json_data:
    d = json.load(json_data)
    json_data.close()

localHost = d["localHost"]
max_posts = d["max_posts"]
# Database parameters initialization for DB connection
db_params = d["db_params"]["localHost"] if localHost else d["db_params"]["Prod"]
DB_USERNAME = db_params["DB_USERNAME"]
DB_PASSWORD = db_params["DB_PASSWORD"]
DB_NAME = db_params["DB_NAME"]
DB_SOCKET = db_params["DB_SOCKET"]
DB_URI = f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}?unix_socket={DB_SOCKET}'

social_media_params = d["params"]["social_media"]
# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app_login = d["login_creds"]
app.secret_key = d["secret_key"]
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # in seconds
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=True)
    message = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(25), nullable=False)
    heading = db.Column(db.String(30), unique=False, nullable=False)
    sub_heading = db.Column(db.String(30), unique=True, nullable=True)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12), nullable=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'active_user' in session:
        return render_template("dashboard.html", social_media_params=social_media_params)
    if request.method == 'POST':
        if request.form.get('uname') == app_login['username'] and request.form.get('upass') == app_login['password']:
            # if app_login['username'] not in session:
            session['active_user'] = app_login['username']
            return render_template("dashboard.html", social_media_params=social_media_params)
    return render_template("login.html")

@app.route("/")
def home():
    post = Posts.query.filter_by().all()[0:max_posts]
    return render_template('index.html', social_media_params=social_media_params, posts=post)

@app.route("/about")
def about():
    return render_template('about.html', social_media_params=social_media_params)

@app.route("/contact", methods=["GET", "POST"])
def save_message():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_mobile = request.form.get("user_mobile")
    user_message = request.form.get("user_message")
    dt = datetime.now()

    if request.method == "POST":
        if user_message != '':
            p = Contact(name=user_name, email=user_email, mobile=user_mobile, message=user_message, date=dt)
            db.session.add(p)
            db.session.commit()
    return render_template('contact.html', social_media_params=social_media_params)

@app.route("/posts/<string:url_slug>", methods=["GET"])
def getPost(url_slug):
    posts = Posts.query.filter_by(slug=url_slug).first()
    return render_template("posts.html", social_media_params=social_media_params, params=posts)


app.run(debug=True)