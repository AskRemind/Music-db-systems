from flask import Blueprint, request, jsonify
from models import db, Song, ListeningHistory

bp = Blueprint('songs', __name__)

@bp.route('/play/<int:song_id>', methods=['POST'])
def play_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404

    history = ListeningHistory(UserID=request.json['user_id'], SongID=song_id)
    db.session.add(history)
    db.session.commit()

    return jsonify({"message": f"Playing {song.Title}"}), 200
