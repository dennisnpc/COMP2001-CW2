from functools import wraps
from flask import request, abort, g
import requests
from config import db
from models import User

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user(email, password):
    response = requests.post(
        AUTH_API_URL,
        json={"email": email, "password": password}
    )

    if response.status_code == 200:
        verification_status = response.json()
        if verification_status == ["Verified", "True"]:
            # Check if user exists in local database
            user = User.query.filter_by(Email=email).first()
            if not user:
                # If not, add user
                user = User(Email=email)
                db.session.add(user)
                db.session.commit()
            return user
    abort(401, "Invalid credentials")

def requires_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        credentials = request.get_json().get("Credentials")
        if not credentials:
            abort(400, "Credentials are required")

        email = credentials.get("Email")
        password = credentials.get("Password")

        if not email or not password:
            abort(400, "Email and Password are required")

        user = authenticate_user(email, password)
        g.current_user = user  # Store the authenticated user in the global context
        return func(*args, **kwargs)
    return wrapper