import json, os, re, requests
from flask import request, Flask, session
from dotenv import load_dotenv

load_dotenv()

client_id = 7
BASE_URL_CHECKING = os.environ.get("BASE_URL_CHECKING")

def checkAdmin():
    url = f"{BASE_URL_CHECKING}/{client_id}"
    
    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}