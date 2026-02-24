from flask import Blueprint, request
import utils.validator as validator
import xmlrpc.client

#I will adjust this to return in the connect() function soon
from db.odoo_connection import connect, ODOO_DB, ODOO_PASSWORD

def signup(jsonRequest):
    
    #  Validate request
    validator.validateRequest(jsonRequest)
    user_data = jsonRequest["user"]  
    application = jsonRequest["application"]

    validator.validateUser(user_data, application)

    #  Connect to Odoo as admin

    uid, models = connect()  # connect() should use admin credentials
    print ("This is the UID:", uid, "This is the models", models)
    
    #  Create res.users record (login account)
    user_id = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.users",
        "create",
        [{
            "name": user_data["name"],
            "login": user_data["login"],
            "password": user_data["password"],  # Odoo will hash automatically
        }]
    )

    # Create hr.employee record linked to the user
    employee_id = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
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

    # Connect to Odoo common endpoint
    common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')

    uid = common.authenticate(application, login, password, {})

    if not uid:
        return {"message": "Invalid login or password"}, 401

    # models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')
    # user_info = models.execute_kw(
    #     application,
    #     uid,
    #     password,
    #     'res.users',
    #     'read',
    #     [uid],
    #     {'fields': ['id', 'name', 'login']}
    # )

    return {
        # "user": user_info,
        "message": "User logged in successfully"
    }, 200
    
