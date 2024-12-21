from flask import Blueprint, request, jsonify
from models import db, UserRating, UserComment
from datetime import datetime

bp = Blueprint('ratings', __name__)

@bp.route('/<int:song_id>', methods=['POST'])
def rate_song(song_id):
    data = request.json
    rating = UserRating(
        UserID=data['user_id'],
        SongID=song_id,
        RatingScore=data['rating']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message": "Song rated successfully!"}), 201

@bp.route('/comments/<int:song_id>', methods=['POST'])
def comment_song(song_id):
    data = request.json
    if len(data['comment']) < 3:
        return jsonify({"error": "Comment is too short"}), 400

    comment = UserComment(
        UserID=data['user_id'],
        SongID=song_id,
        CommentText=data['comment']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201

@bp.route('/ratings/song/<int:song_id>', methods=['GET'])
def get_song_details(song_id):
    song_ratings = db.session.query(db.func.avg(UserRating.RatingScore), db.func.count(UserRating.RatingScore)).filter_by(SongID=song_id).first()
    if not song_ratings or song_ratings[1] == 0:
        return jsonify({
            "average_rating": 0.0,
            "rating_count": 0,
            "comments": []
        })
    comments = UserComment.query.filter_by(SongID=song_id).order_by(UserComment.CommentID.desc()).all()
    return jsonify({
        "average_rating": round(song_ratings[0], 1) if song_ratings[0] else 0.0,
        "rating_count": song_ratings[1],
        "comments": [{"user_id": c.UserID, "comment_text": c.CommentText, "timestamp": c.CommentID} for c in comments]
    })
