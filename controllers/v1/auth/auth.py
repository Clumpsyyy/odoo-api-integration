from flask import Blueprint, request
import utils.validator as validator
from db.odoo_connection import connect

def signup(jsonRequest):
    
    #  Validate request
    validator.validateRequest(jsonRequest)
    user_data = jsonRequest["user"]  
    application = jsonRequest["application"]

    validator.validateUser(user_data, application)

    #  Connect to Odoo as admin
    
    uid, models, ODOO_DB, ODOO_PASSWORD = connect()  # connect() should use admin credentials
    print ("This is the UID:", uid, "This is the models", models)
    
    #  Create res.users record (login account)
    user_id = models.execute_kw(
        ODDO_DB,
        uid,
        ODDO_PASSWORD,
        "res.users",
        "create",
        [{
            "name": user_data["name"],
            "login": user_data["login"],
            "password": user_data["password"],  # Odoo will hash automatically
        }]
    )

    # Create hr.employee record (profile) linked to the user
    employee_id = models.execute_kw(
        ODDO_DB,
        uid,
        ODDO_PASSWORD,
        "hr.employee",
        "create",
        [{
            "name": user_data["name"],
            "work_email": user_data["login"],
            "user_id": user_id,  # link to the res.users account
            # You can add additional fields like membership_plan, phone, etc.
        }]
    )

    return {
        "user_id": user_id,
        "employee_id": employee_id,
        "message": "Member signed up successfully"
    }, 201
    

