from flask import Blueprint, request, jsonify
import utils.validator as validator
from db.odoo_connection import connect, call_kw, ODOO_DB
from flask_jwt_extended import create_access_token

def signup(jsonRequest):
    # Validate request
    validator.validateRequest(jsonRequest)
    user_data = jsonRequest["user"]
    application = jsonRequest["application"]

    validator.validateUser(user_data, application)

    # Authenticate Odoo session (JSON-RPC)
    connect() 

    # Create res.users record (login account)
    user_id = call_kw(
        "res.users",
        "create",
        [{
            "name": user_data["name"],
            "login": user_data["login"],
            "password": user_data["password"],  
        }]
    )

    # Create hr.employee record linked to the user
    employee_id = call_kw(
        "hr.employee",
        "create",
        [{
            "name": user_data["name"],
            "work_email": user_data["login"],
            "user_id": user_id,
        }]
    )

    return {
        "user_id": user_id,
        "employee_id": employee_id,
        "message": "Member signed up successfully"
    }, 201


def login(jsonRequest):
    user_data = jsonRequest["user"]
    application = jsonRequest["application"]

    login = user_data["login"]
    password = user_data["password"]
    
    # return jsonify({"msg:", "invalid credentials"}), 401
    
    # Authenticate user via JSON-RPC
    uid = connect()  # ensure admin session
    session_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": application,
            "login": login,
            "password": password
        },
        "id": 1
    }

    # Use the same requests session from odoo_connection
    import requests
    from db.odoo_connection import session, ODOO_URL

    response = session.post(f"{ODOO_URL}/web/session/authenticate", json=session_payload)
    result = response.json()

    if not result.get("result") or result["result"].get("uid") == 0:
        return {"message": "Invalid login or password"}, 401

    user_uid = result["result"]["uid"]
    
    access_token = create_access_token(identity=login)
    
    # Print the user_info
    user_info = call_kw(
        "res.users",
        "read",
        [[user_uid]],
        {"fields": ["id", "name", "login"]}
    )

    return {
        "user": user_info,
        "message": "User logged in successfully",
        "access_token": access_token,
    }, 200