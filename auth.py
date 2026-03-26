"""
Authentication Module - Handle login, session management, and role-based access
"""

from functools import wraps
from flask import session, redirect, url_for, jsonify
import hashlib
import secrets


# Demo users database (in production, use proper database)
USERS_DB = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "name": "Admin User",
        "email": "admin@disaster.gov"
    },
    "rescue_team": {
        "password": hashlib.sha256("rescue123".encode()).hexdigest(),
        "role": "rescue",
        "name": "Rescue Team Lead",
        "email": "rescue@disaster.gov"
    },
    "public_user": {
        "password": hashlib.sha256("public123".encode()).hexdigest(),
        "role": "public",
        "name": "Public User",
        "email": "user@example.com"
    }
}


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_login(username, password):
    """Verify username and password"""
    if username not in USERS_DB:
        return False, None
    
    user = USERS_DB[username]
    if user["password"] == hash_password(password):
        return True, user
    
    return False, None


def login_user(username, user_data):
    """Create session for user"""
    session["user_id"] = username
    session["username"] = username
    session["role"] = user_data["role"]
    session["name"] = user_data["name"]
    session["email"] = user_data["email"]
    session.permanent = True
    return True


def logout_user():
    """Clear user session"""
    session.clear()
    return True


def is_logged_in():
    """Check if user is logged in"""
    return "user_id" in session


def get_current_user():
    """Get current logged-in user info"""
    if is_logged_in():
        return {
            "user_id": session.get("user_id"),
            "username": session.get("username"),
            "role": session.get("role"),
            "name": session.get("name"),
            "email": session.get("email")
        }
    return None


def get_user_role():
    """Get current user's role"""
    return session.get("role", None)


# Role-based access control decorators

def login_required(f):
    """Require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Require user to be admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        
        if get_user_role() != "admin":
            from flask import render_template
            return render_template('unauthorized.html'), 403
        
        return f(*args, **kwargs)
    return decorated_function


def rescue_required(f):
    """Require user to be rescue team member"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        
        if get_user_role() not in ["rescue", "admin"]:
            from flask import render_template
            return render_template('unauthorized.html'), 403
        
        return f(*args, **kwargs)
    return decorated_function


def public_required(f):
    """Require user to have public access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        
        # Public users and admins can access
        if get_user_role() not in ["public", "admin"]:
            from flask import render_template
            return render_template('unauthorized.html'), 403
        
        return f(*args, **kwargs)
    return decorated_function


def json_login_required(f):
    """Require login for API endpoints (returns JSON)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"error": "Unauthorized", "message": "Please login first"}), 401
        return f(*args, **kwargs)
    return decorated_function


def json_admin_required(f):
    """Require admin role for API endpoints (returns JSON)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"error": "Unauthorized", "message": "Please login first"}), 401
        
        if get_user_role() != "admin":
            return jsonify({"error": "Forbidden", "message": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    return decorated_function
