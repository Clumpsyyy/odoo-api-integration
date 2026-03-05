import json, os, re, requests
from flask import request, Flask, session
from db.odoo_connection import ODOO_DB,uid,ODOO_API_KEY, ODOO_URL, connect, call_kw, session as odoo_session
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("BASE_URL")
AUTH_HEADER = {
    "Authorization": os.environ.get("SECUREPAWS_AUTH"),
    "Content-Type": "application/json"
}

#Register User Account
def RegisterAccount(requestJson, flask_session):
    name = requestJson.get('name')
    phone = requestJson.get('phone')
    password = requestJson.get('password')

    if not name or not phone or not password:
        return {"error": "All fields required"}, 400

    connect()

    # Check duplicate user in user portal
    existing = call_kw("res.users", "search", args=[[["login", "=", phone]]])
    if existing:
        return {"error": "User already exists"}, 400
    
    # Send OTP
    sendOtp(phone)

    flask_session[f"pending_{phone}"] = {"name": name, "password": password}

    return {"message": "OTP sent"}, 200

def verifyOTPAndCreate(requestJson):
    phone = requestJson.get("phoneNumber")
    otp = requestJson.get("otp")

    if not phone or not otp:
        return {"error": "Phone and OTP required"}, 400

    raw_data = session.get(f"pending_{phone}")
    if not raw_data:
        return {"error": "No pending registration or Invalid OTP"}, 400

    data = session.get(f"pending_{phone}") 
    
    # Verify OTP
    if not checkOtp(phone, otp):
        return {"error": "Invalid OTP"}, 400

    connect()

    # Create partner in Odoo
    partner_id = call_kw("res.partner", "create", args=[{
        "name": data["name"],
        "phone": phone
    }])

    # Create user in Odoo
    user_id = call_kw("res.users", "create", args=[{
        "name": data["name"],
        "login": phone,
        "partner_id": partner_id,
        "password": data["password"]
    }])

    # Remove pending registration from session
    session.pop(f"pending_{phone}", None)

    return {"message": "User created successfully"}, 200

# Send OTP
def sendOtp(phoneNumber):
    url = f"{BASE_URL}/get-otp"

    payload = {
        "phoneNumber": phoneNumber
    }

    response = requests.post(url, json=payload, headers=AUTH_HEADER)
    return response.json()

# Verify OTP
def checkOtp(phoneNumber, otp):
    url = f"{BASE_URL}/verify-otp"

    payload = {
        "phoneNumber": phoneNumber,
        "otp": otp
    }

    response = requests.post(url, json=payload, headers=AUTH_HEADER)

    if response.status_code == 200:
        return True
    return False

#Login User Account
def LoginAccount(requestJson):
    login = requestJson.get("phone")
    password = requestJson.get("password")

    if not login or not password:
        return {"error": "Login and password required"}, 400

    try:
        url = f"{ODOO_URL}/web/session/authenticate"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": ODOO_DB,
                "login": login,
                "password": password
            },
            "id": 1
        }
        response = odoo_session.post(url, json=payload)
        result = response.json()
    except Exception as e:
        return {"error": str(e)}, 500

    if "result" in result and result["result"].get("uid"):
        uid = result["result"]["uid"]
        
        access_token = create_access_token(identity=login)
        
        return {"uid": uid, "message": "Login successful", "Token": access_token}, 200

    else:
        return {"error": "Invalid login or password"}, 401
    