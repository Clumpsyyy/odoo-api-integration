from flask import abort
import utils.exception_messages as exception_messages
import db.querys as querys
import re
import requests
import os

def validateRequest(request):
	if(request == None  or request.get("user") == None or request.get("application") == None):
		abort(400, exception_messages.getMsgRequestInvalid())

def validateUser(user, application):
	validateRequiredParametersToCreate(user)
	validateIfUserAlreadyExists(user, application)        

def validateRequiredParametersToCreate(user):
	email = user.get("email")
	username = str(user.get("username"))
	password =  str(user.get("password"))

	if (email == None or not email.strip() or isEmailInvalidByRegex(email) or
		username == None or not username.strip() or len(username) < 4 or
		password == None or not password.strip() or len(password) < 4):
		print("Invalid1")
		abort(400, exception_messages.getMsgRequestInvalid())
		
def validateRequiredParametersToLogin(user):
	email = user.get("email")
	username = str(user.get("username"))
	password =  str(user.get("password"))

	if ((email == None or not email.strip() or isEmailInvalidByRegex(email)) and
		(username == None or not username.strip() or len(username) < 4) or
		password == None or not password.strip() or len(password) < 4):
		print("Invalid2")
		abort(400, exception_messages.getMsgRequestInvalid())

def validateIfUserAlreadyExists(user, application):
	if (querys.getQtdByQuery({"email": user.get("email")}, application) > 0):
		print("Invalid Email")
		abort(400, '')

	if (querys.getQtdByQuery({"username": user.get("username")}, application) > 0):
		print("")
		abort(400, '')

def isEmailInvalidByRegex(email):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) == None

def validateTokenBeforeRequest(token):
	print("")

	if (token == None):
		print("")
		abort(403, exception_messages.getMsgTokenInvalid())
    
	headers = {"authorization": "Bearer " + token}

	url_to_authenticate_token = os.environ.get("URL_TO_AUTHENTICATE_TOKEN", "http://localhost:5000/auth")

	response = requests.get(url_to_authenticate_token, headers=headers)

	if (response.status_code != 200):
		print("Invalid Token")
		abort(response.status_code, response.json()["msg"])

	print("Token Valid")