import requests
import os
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

session = requests.Session()  # keeps cookies (important)
uid = None  # global variable to store authenticated UID

def connect():
    global uid  # Make sure we update the global variable

    url = f"{ODOO_URL}/web/session/authenticate"

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": ODOO_DB,
            "login": ODOO_USERNAME,
            "password": ODOO_PASSWORD
        },
        "id": 1
    }

    response = session.post(url, json=payload)
    result = response.json()

    if result.get("result"):
        uid = result["result"]["uid"]  # ✅ now updates global uid
        print("Authenticated successfully! UID:", uid)
        return uid
    else:
        print("Authentication failed:", result)
        uid = None
        return None
    
def call_kw(model, method, args=None, kwargs=None):
    global uid
    
    if uid is None:
        connect()
        if uid is None:
            raise Exception("Odoo session not authenticated. Call connect() first.")

    url = f"{ODOO_URL}/web/dataset/call_kw"

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args or [],
            "kwargs": kwargs or {}
        },
        "id": 2
    }

    response = session.post(url, json=payload)
    result = response.json()

    if "result" in result:
        return result["result"]
    else:
        raise Exception(f"Odoo JSON-RPC call failed: {result}")