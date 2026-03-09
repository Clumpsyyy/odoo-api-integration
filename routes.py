import controllers.v1.auth.auth as auth
import controllers.v1.transaction as transaction
import services.checkAdmin as adminCheck
import utils.exception_messages as exception_messages
import utils.validator as validator
from flask import abort, Blueprint, Flask, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity #jwt import
from limits import RateLimitItemPerSecond
from limits.strategies import FixedWindowRateLimiter
from limits.storage import MemoryStorage
from controllers.v1.transaction import getTransaction

auth_bp = Blueprint('auth_bp', __name__)

storage = MemoryStorage()
limiter = FixedWindowRateLimiter(storage)
limit = RateLimitItemPerSecond(1) 

@auth_bp.route("/create", methods=['POST'])
def createData():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429
    
    try:
        result, status = auth.RegisterAccount(request.json, session)
        print("Register request:", request.json)
        print("Save Session", session)
    except Exception as e:
        return jsonify({"error1": str(e)}), 500

    return jsonify({"user": result}), status

@auth_bp.route("/verify-otp", methods=['POST'])
def verify_otp():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429

    try:
        result, status = auth.verifyOTPAndCreate(request.json)
        print("verifyOTPAndCreate request:", request.json)
    except Exception as e:
        return jsonify({"error2": str(e)}), 500

    return jsonify(result), status

@auth_bp.route("/login", methods=['POST'])
def userLogin():
    
    data = request.json
    print("Request JSON:", data)

    response = adminCheck.checkAdmin()
    print("response", response)

    if response.get("status") != "Active":
        return jsonify({"error": "Server is down"}), 403
    
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429

    result, status = auth.LoginAccount(request.json)
    print("request", request.json)
    
    if not isinstance(result, dict):
        result = {"error": "Unexpected server response"}

    return jsonify(result), status

data_bp = Blueprint('data_bp', __name__)

@data_bp.route("/createTransaction", methods=['POST'])
@jwt_required()
def createTransaction():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429
    result, status = transaction.createTransaction(request.json)
    
    payment_id = result["payment_id"]

    transaction_data = getTransaction(payment_id)
    return jsonify({"Transaction Details": transaction_data}), status

# @data_bp.route("/GetTransaction/{payment_id}", methods=['GET'])
# def getTransaction():
#     if not limiter.hit(limit):
#         return jsonify({"error": "Too many requests"}), 429
#     result, status = log.getTransaction(request.json)
#     return jsonify({"Transaction Received by the system": result}), status
# .
