from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
import models 
import os
from flask import g

from api.user import user 
from api.api import api
from api.check_green import check_green
DEBUG = True
PORT = 8000

login_manager = LoginManager()


# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'BARBEQUE SAUCE'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
   try:
      return models.User.get(models.User.id == userid)
   except models.DoesNotExist:
      return None

CORS(api, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(check_green, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(api)
app.register_blueprint(check_green)

@app.before_request
def before_request():
   """Connect to the database before each request"""
   g.db = models.DATABASE
   g.db.connect()

@app.after_request
def after_request(response):
   g.db.close()
   return response 


@app.route('/')
def index():
    return 'box shrubs 4 eva'

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

# Run the app when the program starts!
if __name__ == '__main__':
   models.initialize()
   app.run(debug=DEBUG, port=PORT)

