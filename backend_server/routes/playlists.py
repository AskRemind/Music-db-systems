from flask import Blueprint, request, jsonify
from models import db, Playlist, PlaylistSong, Song

bp = Blueprint('playlists', __name__)

# Helper function to check user authentication
def get_user_id():
    user_id = request.headers.get('UserID')
    if not user_id:
        return None
    return user_id

# Ensure the user provides UserID before accessing these endpoints
@bp.before_request
def require_user_id():
    if request.method == 'OPTIONS':
        return '', 200
    if not get_user_id():
        return jsonify({"error": "UserID must be provided in headers to perform this action."}), 401

@bp.route('/', methods=['GET', 'POST'])
def playlists():
    if request.method == 'GET':
        user_id = get_user_id()
        playlists = Playlist.query.filter_by(UserID=user_id).all()
        playlist_list = [{"playlist_id": p.PlaylistID, "title": p.Title} for p in playlists]
        return jsonify(playlist_list), 200

    if request.method == 'POST':
        data = request.json
        user_id = get_user_id()
        if not data.get('title'):
            return jsonify({"error": "Playlist title cannot be empty."}), 400
        new_playlist = Playlist(UserID=user_id, Title=data['title'], Description=data.get('description', ''))
        db.session.add(new_playlist)
        db.session.commit()
        return jsonify({"message": "Playlist created successfully!", "playlist_id": new_playlist.PlaylistID}), 201

@bp.route('/<int:playlist_id>/add-song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    data = request.json
    song_id = data['song_id']
    user_id = get_user_id()

    playlist = Playlist.query.filter_by(PlaylistID=playlist_id, UserID=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found or access denied."}), 404

    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found."}), 404

    new_entry = PlaylistSong(PlaylistID=playlist_id, SongID=song_id)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Song added to playlist!"}), 200

@bp.route('/<int:playlist_id>/songs', methods=['GET'])
def get_playlist_songs(playlist_id):
    user_id = get_user_id()
    playlist = Playlist.query.filter_by(PlaylistID=playlist_id, UserID=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found or access denied."}), 404

    songs = (db.session.query(Song)
             .join(PlaylistSong, Song.SongID == PlaylistSong.SongID)
             .filter(PlaylistSong.PlaylistID == playlist_id)
             .all())

    song_list = [{"song_id": song.SongID, "title": song.Title, "artist_id": song.ArtistID} for song in songs]
    return jsonify({"playlist": playlist.Title, "songs": song_list}), 200

@bp.route('/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    user_id = get_user_id()
    playlist = Playlist.query.filter_by(PlaylistID=playlist_id, UserID=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found or access denied."}), 404

    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist deleted successfully!"}), 200

@bp.route('/<int:playlist_id>/remove-song', methods=['DELETE'])
def remove_song_from_playlist(playlist_id):
    data = request.json
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "UserID must be provided."}), 401

    song_id = data.get('song_id')
    if not song_id:
        return jsonify({"error": "Song ID must be provided."}), 400

    playlist = Playlist.query.filter_by(PlaylistID=playlist_id, UserID=user_id).first()
    if not playlist:
        return jsonify({"error": "Playlist not found or access denied."}), 404

    playlist_song = PlaylistSong.query.filter_by(PlaylistID=playlist_id, SongID=song_id).first()
    if not playlist_song:
        return jsonify({"error": "Song not found in the playlist."}), 404

    db.session.delete(playlist_song)
    db.session.commit()

    return jsonify({"message": "Song removed from playlist!"}), 200

