from flask import abort
import utils.exception_messages as exception_messages
import db.querys as querys
import re
import requests
import os


def validateRequest(request):
    if not request or not request.get("user"):
        abort(400, exception_messages.getMsgRequestInvalid())

def validateUserInput(user):
    validateRequiredParametersToCreate(user)

def validateRequiredParametersToCreate(user):
    name = user.get("name")
    email = user.get("email")
    phone = user.get("phone")

    if (
        not name or not str(name).strip() or
        not email or not str(email).strip() or isEmailInvalidByRegex(email) or
        not phone or not phone.strip() or len(phone) < 12
    ):
        abort(400, exception_messages.getMsgRequestInvalid())

def validateRequiredParametersToLogin(user):
    login = user.get("login")
    password = user.get("password")

    if (
        (not login or not str(login).strip()) or
        (not password or not str(password).strip() or len(password) < 4)
    ):
        abort(400, exception_messages.getMsgRequestInvalid())

# def validateIfUserAlreadyExists(user, application):
#     # Check by login (email)
#     if querys.getQtdByQuery({"login": user.get("login")}, application) > 0:
#         abort(400, "User with this login already exists")

def isEmailInvalidByRegex(email):
    return re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        email
    ) is None

# def validateTokenBeforeRequest(token):
#     if not token:
#         abort(403, exception_messages.getMsgTokenInvalid())

#     headers = {"authorization": "Bearer " + token}

#     url_to_authenticate_token = os.environ.get(
#         "URL_TO_AUTHENTICATE_TOKEN",
#         "http://localhost:5000/auth"
#     )

#     response = requests.get(url_to_authenticate_token, headers=headers)

#     if response.status_code != 200:
#         abort(response.status_code, response.json().get("msg", "Invalid token"))