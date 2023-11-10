from api.config.config import Config
from flask import Flask, render_template, session, redirect, url_for, abort
from flask_cors import CORS
from functools import wraps
import pymongo


app = Flask(__name__, template_folder="../templates",
            static_folder="../static")


app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE
app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE

CORS(app, resources={r"/api/*": {"origins": ["http://localhost",
                     "http://127.0.0.1"], "supports_credentials": True}})

# Database
client = pymongo.MongoClient(Config.MONGO_URI)
db = client.get_default_database()


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login/')

    return wrap

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session and session['user'].get('role') == 'admin':
            return f(*args, **kwargs)
        else:
            abort(403)  # Forbidden status
    return decorated_function


@app.route('/')
def home():
    return render_template('home.html')


# Import routes after app and db are defined
from .routes.user_routes import *
from .routes.vehicle_routes import *
from .routes.tracking_routes import *
from .routes.admin_routes import *


if __name__ == "__main__":
    app.run(debug=True)
