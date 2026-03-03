from flask import request, Flask, jsonify
import requests
from db.odoo_connection import ODOO_DB,uid,ODOO_API_KEY, ODOO_URL, connect, call_kw, session
from datetime import datetime
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def createTransaction(requestJson):

    accountNumber = requestJson.get("accountNumber")
    amount = requestJson.get("amount")
    accountName = requestJson.get("accountName")

    if not accountNumber or len(accountNumber) < 8:
        return {"error": "Must be 8 numbers"}, 400

    if not amount or float(amount) <= 0:
        return {"error": "Invalid amount"}, 400

    uid = connect()

    if not uid:
        return {"error": "Authentication failed"}, 500

    search_partner_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                uid,
                ODOO_API_KEY,
                "res.partner",
                "search",
                [[["name", "=", accountName]]]
            ]
        },
        "id": 1
    }

    partner_response = requests.post(f"{ODOO_URL}/jsonrpc", json=search_partner_payload).json()

    if not partner_response.get("result"):
        return {"error": "Username doesn't match to the database"}, 404

    partner_id = partner_response["result"][0]

    search_journal_payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            ODOO_DB,
            uid,
            ODOO_API_KEY,
            "account.journal",
            "search_read",
            [[["type", "=", "bank"], ["name", "ilike", "Bank"]]],
            {"fields": ["id", "name"]}
        ]
    },
    "id": 1
    }

    journal_response = requests.post(f"{ODOO_URL}/jsonrpc", json=search_journal_payload).json()

    if not journal_response.get("result"):
        return {"error": "No matching journal found"}, 404

    journal_id = journal_response["result"][0]["id"]
    print("test journal_id", journal_id)
        
    search_method_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                uid,
                ODOO_API_KEY,
                "account.payment.method.line",
                "search_read",
                [  
                [
                        ["journal_id", "=", journal_id]
                    ]
                ],
                {"fields": ["id", "name", "payment_type"]}
            ]
        },
        "id": 10
    }
    method_response = requests.post(f"{ODOO_URL}/jsonrpc", json=search_method_payload).json()

    if not method_response.get("result"):
        return {"error": "No valid payment method for this journal"}, 400

    payment_method_line_id = method_response["result"][0]["id"]
    print("Using payment method line ID:", payment_method_line_id)
    
    payment_date = datetime.today().strftime('%Y-%m-%d')
    
    payment_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                uid,
                ODOO_API_KEY,
                "account.payment",
                "create",
                [{
                    "payment_type": "inbound",
                    "partner_type": "customer",
                    "partner_id": partner_id,
                    "amount": float(amount),
                    "date": payment_date,
                    "journal_id": journal_id, 
                    "payment_method_line_id": payment_method_line_id,  
                }]
            ]
        },
        "id": 2
    } 

    payment_response = requests.post(f"{ODOO_URL}/jsonrpc", json=payment_payload).json()

    if "error" in payment_response:
        return {"error": payment_response["error"]}, 500

    payment_id = payment_response["result"]
    
    
    post_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                uid,
                ODOO_API_KEY,
                "account.payment",
                "action_post",
                [[payment_id]]
            ]
        },
        "id": 3
    }

    requests.post(f"{ODOO_URL}/jsonrpc", json=post_payload)

    return {
        "message": "Payment successfully created and posted",
        "payment_id": payment_id
    }, 201
    
def getTransaction(payment_id):
    payments = call_kw(
        "account.payment",
        "search_read",
        [[["id", "=", payment_id]]],
        {"fields": ["id", "partner_id", "amount", "state"]}
    )

    if not payments:
        return {"error": "Payment not found"}, 404

    payment = payments[0]
    partner_id, partner_name = payment["partner_id"]

    return {
        "payment_id": payment["id"],
        "partner_id": partner_id,
        "partner_name": partner_name,
        "amount": payment["amount"],
        "state": payment["state"]
    }, 200