from flask import Flask
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

# Create SQLAlchemy engine
db = SQLAlchemy(app)

# Optional: Define your database models using db.Model here
# For example:
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    useremail = db.Column(db.String(50), unique=False, nullable=False)
    usermobile = db.Column(db.String(10), unique=True, nullable=True)
    usermessage = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)



# Ensure to create tables if needed
# db.create_all()

# Define routes and other Flask application code below
# Example:
@app.route('/')
def index():
    name = 'aman'
    email = 'aman@123'
    mobile = '9091929394'
    mssg = 'Hi'
    dt = datetime.now()
    p = Contact(username=name, useremail=email, usermobile=mobile, usermessage = mssg, date=dt)
    db.session.add(p)
    db.session.commit()
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
