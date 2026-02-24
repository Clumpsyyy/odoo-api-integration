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

#Sign Up Endpoint
@auth_bp.route("/signup", methods=['POST'])
def createNewUser():
    response = auth.signup(request.json)
    return jsonify(response), 201

#Sign In Endpoint
@auth_bp.route("/login", methods=['POST'])
def login():
    return jsonify({"user": auth.login(request.json)})

member_bp = Blueprint('member_bp', __name__)

#Check List of member Endpoint
@member_bp.route("/check", methods=['POST'])
def showMember():
    result = member.ShowMember(request.json)
    return jsonify({"user": result})

#Add member/ Create member Endpoint
@member_bp.route("/add", methods=['POST'])
def addMember():
    result = member.AddMember(request.json)
    return jsonify({"user": result})

#Update member endpoint
@member_bp.route("/update", methods=['PUT'])
def updateMember(): 
    result = member.UpdateMember(request.json)
    return jsonify({"user": result})

#Delete Member endpoint
@member_bp.route("/delete", methods=['DELETE'])
def deleteMember():
    result = member.DeleteMember(request.json)
    return jsonify({"user": result})

#Error Handling Endpoint
@member_bp.errorhandler(404)
def errorHandler(error):
    return error