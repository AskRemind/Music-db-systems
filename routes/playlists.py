from flask import Blueprint, request, jsonify
from models import db, Playlist, PlaylistSong

bp = Blueprint('playlists', __name__)

@bp.route('/', methods=['POST'])
def create_playlist():
    data = request.json
    new_playlist = Playlist(UserID=data['user_id'], Title=data['title'], Description=data.get('description', ''))
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({"message": "Playlist created successfully!", "playlist_id": new_playlist.PlaylistID}), 201

@bp.route('/<int:playlist_id>/add-song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    data = request.json
    new_entry = PlaylistSong(PlaylistID=playlist_id, SongID=data['song_id'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Song added to playlist!"}), 200

@bp.route('/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist deleted successfully!"}), 200
