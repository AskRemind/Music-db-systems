from flask import Blueprint, request, jsonify
from models import db, Subscription, User
from datetime import datetime

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
    user_id = data.get('user_id')
    plan_type = data.get('plan_type')
    start_date_str = data.get('start_date')

    # Validate input
    if not user_id or not plan_type or not start_date_str:
        return jsonify({"error": "Missing required fields"}), 400

    # Validate user existence
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Invalid user ID"}), 404

    # Validate plan type
    valid_plans = {"Free", "Premium", "Family"}
    if plan_type not in valid_plans:
        return jsonify({"error": "Invalid plan type"}), 400

    # Validate start date
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if start_date < datetime.now().date():
            return jsonify({"error": "Start date cannot be in the past"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Check for existing active subscription
    active_subscription = Subscription.query.filter_by(UserID=user_id, IsActive=True).first()
    if active_subscription:
        return jsonify({"error": "User already has an active subscription"}), 409

    # Create new subscription
    new_subscription = Subscription(
        UserID=user_id,
        PlanType=plan_type,
        StartDate=start_date,
        IsActive=True
    )
    db.session.add(new_subscription)
    db.session.commit()

    return jsonify({
        "message": "Subscription successful!",
        "subscription": {
            "UserID": new_subscription.UserID,
            "PlanType": new_subscription.PlanType,
            "StartDate": new_subscription.StartDate.isoformat()
        }
    }), 201

@bp.route('/users/<user_id>/subscription', methods=['GET'])
def get_subscription(user_id):
    subscription = Subscription.query.filter_by(UserID=user_id, IsActive=True).first()
    if not subscription:
        return jsonify({"error": "No active subscription"}), 404

    return jsonify({
        "UserID": subscription.UserID,
        "PlanType": subscription.PlanType,
        "StartDate": subscription.StartDate.isoformat()
    }), 200


