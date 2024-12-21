from flask import Blueprint, request, jsonify
from models import db, Song, ListeningHistory, Artist
from datetime import datetime
import random
bp = Blueprint('songs', __name__)

@bp.route('/play/<int:song_id>', methods=['POST'])
def play_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404

    start_time = datetime.utcnow()
    history = ListeningHistory(UserID=request.json['user_id'], SongID=song_id, StartTime=start_time)

    db.session.add(history)
    db.session.commit()

    return jsonify({"message": f"Playing {song.Title}", "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S')}), 200

@bp.route('/history/<int:user_id>', methods=['GET'])
def get_play_history(user_id):
    history = db.session.query(ListeningHistory, Song).join(Song, ListeningHistory.SongID == Song.SongID).filter(
        ListeningHistory.UserID == user_id
    ).all()

    if not history:
        return jsonify({"error": "No play history found"}), 404

    return jsonify([song.Title for _, song in history]), 200

@bp.route('/daily-recommendation', methods=['GET'])
def daily_recommendation():
    try:
        all_songs = Song.query.all()
        all_artists = Artist.query.all()

        if not all_songs:
            return jsonify({"error": "No songs available"}), 404

        if len(all_songs) <= 10:
            random_songs = all_songs
        else:
            random_songs = random.sample(all_songs, 10)

        artist_map = {artist.ArtistID: artist.Name for artist in all_artists}

        songs_data = []
        for song in random_songs:
            artist_name = artist_map.get(song.ArtistID, "Unknown Artist")
            songs_data.append({
                "song_id": song.SongID,
                "title": song.Title,
                "artist_name": artist_name
            })

        return jsonify(songs_data), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@bp.route('/search', methods=['GET'])
def search_songs():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "No search query provided"}), 400
    songs = Song.query.filter(Song.Title.ilike(f"%{query}%")).all()
    result = [{"SongID": song.SongID, "Title": song.Title} for song in songs]
    return jsonify(result)







