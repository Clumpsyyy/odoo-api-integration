from flask import abort, Blueprint, Flask, request, jsonify
import controllers.v1.log as log
import utils.exception_messages as exception_messages
import utils.validator as validator
from flask_jwt_extended import jwt_required, get_jwt_identity
from limits import RateLimitItemPerSecond
from limits.strategies import FixedWindowRateLimiter
from limits.storage import MemoryStorage

data_bp = Blueprint('data_bp', __name__)

storage = MemoryStorage()
limiter = FixedWindowRateLimiter(storage)
limit = RateLimitItemPerSecond(1) 

@data_bp.route("/create", methods=['POST'])
def createData():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429
    result, status = log.createUserData(request.json)
    return jsonify({"user": result}), status

@data_bp.route("/createTransaction", methods=['POST'])
def createTransaction():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429
    result, status = log.createTransaction(request.json)
    return jsonify({"Transaction Details": result}), status

@data_bp.route("/GetTransaction", methods=['GET'])
def getTransaction():
    if not limiter.hit(limit):
        return jsonify({"error": "Too many requests"}), 429
    result, status = log.getTransaction(request.json)
    return jsonify({"Transaction Received by the system": result}), status
