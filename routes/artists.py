from flask import Blueprint, jsonify
from models import Artist

bp = Blueprint('artists', __name__)

@bp.route('/', methods=['GET'])
def get_all_artists():
    artists = Artist.query.all()
    return jsonify([{
        "ArtistID": artist.ArtistID,
        "Name": artist.Name,
        "Country": artist.Country
    } for artist in artists]), 200
