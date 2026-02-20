#import necesssary package 
from flask import Flask
from routes import auth_bp, member_bp
import db.odoo_connection as connection


#authenticate login and signup
# from controllers.v1.auth.auth import auth_bp
# from controllers.v1.member import member_bp

app = Flask(__name__)

#api route for authentication
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

#api route for members
app.register_blueprint(member_bp, url_prefix="/api/v1/member")

# Test Odoo connection first
try:
    uid, models = connection.connect()
    print("Connected successfully! UID:", uid)
except Exception as e:
    print("Connection failed:", e)
    
#main
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
