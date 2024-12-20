from flask import Blueprint, request, jsonify
from models import db, Subscription

bp = Blueprint('subscriptions', __name__)

@bp.route('/plans', methods=['GET'])
def get_plans():
    plans = [
        {"PlanType": "Free", "Price": 0},
        {"PlanType": "Premium", "Price": 9.99},
        {"PlanType": "Family", "Price": 14.99},
    ]
    return jsonify(plans), 200

@bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    new_subscription = Subscription(
        UserID=data['user_id'],
        PlanType=data['plan_type'],
        StartDate=data['start_date'],
        IsActive=True
    )
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify({"message": "Subscription successful!"}), 201
