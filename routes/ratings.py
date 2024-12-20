from flask import Blueprint, request, jsonify
from models import db, UserRating, UserComment

bp = Blueprint('ratings', __name__)

@bp.route('/<int:song_id>', methods=['POST'])
def rate_song(song_id):
    data = request.json
    rating = UserRating(UserID=data['user_id'], SongID=song_id, RatingScore=data['rating'], RatingDate=data['date'])
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message": "Song rated successfully!"}), 201

@bp.route('/comments/<int:song_id>', methods=['POST'])
def comment_song(song_id):
    data = request.json
    if len(data['comment']) < 3:
        return jsonify({"error": "Comment is too short"}), 400
    comment = UserComment(UserID=data['user_id'], SongID=song_id, CommentText=data['comment'], CommentDate=data['date'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201
