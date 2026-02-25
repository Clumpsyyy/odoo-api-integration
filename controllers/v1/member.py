from flask import Blueprint, request
from db.odoo_connection import connect, call_kw

def ShowMember():
    # Make sure session is authenticated
    connect()

    # Search all users
    user_ids = call_kw(
        "res.users",
        "search",
        [[]]
    )

    if not user_ids:
        return {"members": []}, 200

    # Read specific fields
    members = call_kw(
        "res.users",
        "read",
        [user_ids],
        {"fields": ["id", "name", "login"]}
    )

    return {"members": members}, 200

# def AddMember(jsonRequest):
    
#     return {"message": "Member endpoint" }, 200
# def DeleteMember(jsonRequest):
    
#     return {"message": "Member endpoint" }, 200
# def UpdateMember(jsonRequest):
    
#     return {"message": "Member endpoint" }, 200
 