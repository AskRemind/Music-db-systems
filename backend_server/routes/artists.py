from flask import Blueprint, jsonify
from models import  Artist
import random

bp = Blueprint('artists', __name__)

@bp.route('/daily-artist-recommendation', methods=['GET'])
def daily_artist_recommendation():
    try:
        all_artists = Artist.query.all()

        if not all_artists:
            return jsonify({"error": "No artists available"}), 404

        if len(all_artists) <= 10:
            random_artists = all_artists
        else:
            random_artists = random.sample(all_artists, 10)

        artists_data = [
            {
                "artist_id": artist.ArtistID,
                "name": artist.Name,
            }
            for artist in random_artists
        ]

        return jsonify(artists_data), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500