from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Replace with your actual MySQL username, password, database name, and socket path
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_NAME = 'BlogApp'
DB_SOCKET = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}?unix_socket={DB_SOCKET}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=True)
    message = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return (render_template('about.html'))

@app.route("/contact", methods=["GET", "POST"])
def saveMessage():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_mobile = request.form.get("user_mobile")
    user_message = request.form.get("user_message")
    dt = datetime.now()

    if request.method == "GET":
        return render_template('contact.html')
    if user_message != '':
        p = Contact(name=user_name, email=user_email, mobile=user_mobile, message = user_message, date=dt)
        db.session.add(p)
        db.session.commit()
    return redirect('/')

app.run(debug=True)