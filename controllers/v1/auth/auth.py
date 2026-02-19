from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    return {"message": "login endpoint" }, 200

@auth_bp.route("/signup", methods=["POST"])
def signup():
    return {"message": "Signup endpoint" }, 200