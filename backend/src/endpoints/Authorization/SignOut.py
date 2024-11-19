from flask import Blueprint, jsonify
from flask_login import logout_user, current_user
from flask import current_app

sign_out_bp = Blueprint("sign_out", __name__)


@sign_out_bp.route("/authorization/sign_out", methods=["POST"])
def sign_out():
    """Sign out
    ---
    responses:
      200:
        description: Sign out successful
      401:
        description: User not logged in
    """
    if not current_user.is_authenticated:
        current_app.logger.info("Sign out failed: User not logged in")
        return jsonify({"error": "User not logged in"}), 401

    current_app.logger.info(f"Sign out: {current_user.username}")

    logout_user()

    return jsonify({"message": "Sign out successful"}), 200
