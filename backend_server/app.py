from flask import Flask
from flask_migrate import Migrate
from models import db, init_db
from routes.users import bp as users_bp
from routes.subscriptions import bp as subscriptions_bp
from routes.songs import bp as songs_bp
from routes.artists import bp as artists_bp
from routes.playlists import bp as playlists_bp
#from routes.recommendations import bp as recommendations_bp
from routes.ratings import bp as ratings_bp
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'simple_secret_key'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Initialize database and blueprints
init_db(app)
migrate = Migrate(app, db)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
app.register_blueprint(songs_bp, url_prefix='/songs')
app.register_blueprint(artists_bp, url_prefix='/artists')
app.register_blueprint(playlists_bp, url_prefix='/playlists')
#app.register_blueprint(recommendations_bp, url_prefix='/recommendations')
app.register_blueprint(ratings_bp, url_prefix='/ratings')

if __name__ == '__main__':
    app.run(debug=True)