from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from routes.users import bp as users_bp
from routes.subscriptions import bp as subscriptions_bp
from routes.songs import bp as songs_bp
from routes.playlists import bp as playlists_bp
#from routes.recommendations import bp as recommendations_bp#
#Add recommendations data#
from routes.ratings import bp as ratings_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
app.register_blueprint(songs_bp, url_prefix='/songs')
app.register_blueprint(playlists_bp, url_prefix='/playlists')

#Fix this after you have added recommendations#
#app.register_blueprint(recommendations_bp, url_prefix='/recommendations')#
app.register_blueprint(ratings_bp, url_prefix='/ratings')


if __name__ == '__main__':
    app.run(debug=True)

