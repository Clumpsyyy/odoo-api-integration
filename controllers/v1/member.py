from flask import Blueprint

member_bp = Blueprint("member", __name__)

@member_bp.route("/checkMember", methods=["POST"])
def checkMember():
    return {"message": "Member endpoint" }, 200