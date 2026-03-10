import json, os, re, requests
from flask import request, Flask, session
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID= os.environ.get("CLIENT_ID")
BASE_URL_CHECKING = os.environ.get("BASE_URL_CHECKING")

def checkAdmin():
    url = f"{BASE_URL_CHECKING}/{CLIENT_ID}"
    
    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}