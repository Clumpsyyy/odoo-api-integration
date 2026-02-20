from flask import Blueprint, request

def checkMember(jsonRequest):
    return {"message": "Member endpoint" }, 200