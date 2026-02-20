from flask import abort, Blueprint, Flask, request, jsonify
import controllers.v1.auth.auth as auth
import controllers.v1.member as member
import utils.exception_messages as exception_messages
import utils.validator as validator

auth_bp = Blueprint('auth_bp', __name__)

# @app_blueprint.route("/onboarding")
# def defaultRoute():
#     return "Yes, it works!"

# @app_blueprint.before_request
# def verifyToken():
#     if request.path != "/itWorks":
#         token = request.headers.get("authorization")
#         validator.validateTokenBeforeRequest(token)

@auth_bp.route("/signup", methods=['POST'])
def createNewUser():
	idCreated = auth.signup(request.json)
	return jsonify({"userCreatedId": idCreated})

@auth_bp.route("/login", methods=['POST'])
def loginUser():
    return jsonify({"user": auth.login(request.json)})

member_bp = Blueprint('member_bp', __name__)

@member_bp.route("/checkMember", methods=['POST'])
def ShowMember():
    result = member.checkMember(request.json)
    return jsonify({"user": result})

@member_bp.errorhandler(404)
def errorHandler(error):
    return error