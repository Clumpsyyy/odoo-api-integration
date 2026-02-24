import xmlrpc.client
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


def connect():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    
    if uid:
        print("Authenticated successfully! UID:", uid)
        print("Authenticated successfully! models:", models)
        # print("Authenticated successfully! UID:", ODOO_DB)
        # print("Authenticated successfully! models:", ODOO_PASSWORD)
        # Get Odoo version info
        version_info = common.version()
        print("Odoo version info:", version_info)
    else:
        print("Authentication failed")
    
    return uid, models
    