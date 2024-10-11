from flask import Flask, request, jsonify
from flasgger import Swagger
from backend import *



app = Flask(__name__)


# Database
DATABASE_URI = 'postgresql://husic:husic@localhost:5432/iis'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Init app
db.init_app(app)

swagger = Swagger(app)

# Create tables
with app.app_context():
  db.create_all()

# Register blueprints(endpoints)
app.register_blueprint(create_caretaker_bp)
app.register_blueprint(create_walking_schedule_bp)
app.register_blueprint(create_animal_bp)


    
    


if __name__ == '__main__':
  app.run(debug=True)
