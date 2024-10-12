from flask import Flask, request, jsonify
from flask_login import LoginManager
from flasgger import Swagger
from backend import *



app = Flask(__name__)


# Database
DATABASE_URI = 'postgresql://husic:husic@localhost:5432/iis'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'husic'  # Tajný klíč pro session





# Init app
db.init_app(app)
swagger = Swagger(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# login_manager.login_view = 'sign in'



# Create tables
with app.app_context():
  db.create_all()

# Register blueprints(endpoints)
app.register_blueprint(create_caretaker_bp)
app.register_blueprint(create_walking_schedule_bp)
app.register_blueprint(create_animal_bp)
app.register_blueprint(sign_in_bp)
app.register_blueprint(sign_up_bp)


    
    


if __name__ == '__main__':
  app.run(debug=True)
