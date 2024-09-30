from flask import Flask
from models import db
import os


app = Flask(__name__)

# SQLite database
DATABASE_URI = 'postgresql://husic:husic@localhost:5432/iis'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init app
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
