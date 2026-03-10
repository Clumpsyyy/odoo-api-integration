import os
import db.odoo_connection as connection
from flask import Flask
from routes import auth_bp, data_bp
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.permanent_session_lifetime = timedelta(minutes=5)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
app.register_blueprint(data_bp, url_prefix="/api/v1/transaction")

#This comment is intended for integration
# app.use(cors({
#   origin: "https://your-frontend.vercel.app"}))

# Authenticate Odoo
try:
    uid = connection.connect() 
    if uid:
        print("Connected to Odoo successfully! UID:", uid)
    else:
        print("Odoo authentication failed")
except Exception as e:
    print("Odoo connection failed:", str(e))

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)