from flask import request, Flask, jsonify
import requests
from db.odoo_connection import ODOO_DB,uid,ODOO_API_KEY, ODOO_URL, connect, call_kw, session
from datetime import datetime
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

#Register User Account
def RegisterAccount(requestJson):
    name = requestJson.get('name')
    phone = requestJson.get('phone')
    password = requestJson.get('password')

    if not name:
        return {"error": "Name is required"}, 400
    if not phone or not password:
        return {"error": "Phone and password are required"}, 400

    connect()

    # Check duplicate
    existing = call_kw("res.users", "search", args=[[["login", "=", phone]]])
    if existing:
        return {"error": "User already exists"}, 400

    # Create partner
    partner_id = call_kw("res.partner", "create", args=[{"name": name, "phone": phone}])

    # Create user 
    user_id = call_kw("res.users", "create", args=[{
        "name": name,
        "login": phone,
        "partner_id": partner_id,
        "password": password
    }])

    return {"message": "User created successfully", "user_id": user_id}, 200

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
        response = session.post(url, json=payload)
        result = response.json()
    except Exception as e:
        return {"error": str(e)}, 500

    if "result" in result and result["result"].get("uid"):
        uid = result["result"]["uid"]
        
        access_token = create_access_token(identity=login)
        
        return {"uid": uid, "message": "Login successful", "Token": access_token}, 200

    else:
        return {"error": "Invalid login or password"}, 401
    

