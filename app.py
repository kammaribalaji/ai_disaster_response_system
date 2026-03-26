from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import secrets

# =========================
# IMPORT ROUTES
# =========================
from routes.predict import predict_bp
from routes.map import map_bp
from routes.route_opt import route_bp
from routes.dashboard import dashboard_bp
from routes.report import report_bp
from routes.relief import relief_bp
from routes.chat import chat_bp
from routes.tasks import tasks_bp

# =========================
# IMPORT AUTH
# =========================
from auth import verify_login, login_user, get_current_user, login_required, admin_required, rescue_required, public_required

# =========================
# DATABASE INIT
# =========================
from database.db import init_db

# =========================
# APP CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'frontend'),
    static_folder=os.path.join(BASE_DIR, 'frontend', 'assets'),
    static_url_path='/assets'
)

# Session config
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Reload templates automatically (dev + helpful in deploy)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# =========================
# INITIALIZE DATABASE
# =========================
init_db()

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(predict_bp)
app.register_blueprint(map_bp)
app.register_blueprint(route_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(relief_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(tasks_bp)

# =========================
# ROUTES (FRONTEND PAGES)
# =========================

@app.route('/')
def index():
    """Home route - redirects to login or dashboard based on session"""
    user = get_current_user()
    if user:
        # Redirect to role-specific dashboard
        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user['role'] == 'rescue':
            return redirect(url_for('rescue_dashboard'))
        else:
            return redirect(url_for('public_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route - handles both login page display and authentication"""
    if request.method == 'GET':
        user = get_current_user()
        if user:  # Redirect if already logged in
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='Username and password required'), 400
        
        is_valid, user_data = verify_login(username, password)
        if is_valid and user_data:
            login_user(username, user_data)
            # Redirect to role-specific dashboard
            if user_data['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user_data['role'] == 'rescue':
                return redirect(url_for('rescue_dashboard'))
            else:
                return redirect(url_for('public_dashboard'))
        
        return render_template('login.html', error='Invalid username or password'), 401



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout route - clears session and redirects to login"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Default dashboard - redirects to role-specific dashboard"""
    user = get_current_user()
    if user['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif user['role'] == 'rescue':
        return redirect(url_for('rescue_dashboard'))
    else:
        return redirect(url_for('public_dashboard'))


@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard - full system overview"""
    user = get_current_user()
    return render_template('admin_dashboard_new.html', user=user)


@app.route('/rescue-dashboard')
@rescue_required
def rescue_dashboard():
    """Rescue team dashboard - mission coordination"""
    user = get_current_user()
    return render_template('rescue_dashboard_new.html', user=user)


@app.route('/public-dashboard')
@public_required
def public_dashboard():
    """Public dashboard - safety information"""
    user = get_current_user()
    return render_template('public_dashboard_new.html', user=user)


@app.route('/prediction')
@app.route('/predict')
@login_required
def prediction():
    user = get_current_user()
    return render_template('prediction.html', user=user)


@app.route('/routes')
@admin_required
def routes_page():
    user = get_current_user()
    return render_template('routes.html', user=user)


@app.route('/relief')
@login_required
def relief_page():
    user = get_current_user()
    return render_template('relief.html', user=user)


@app.route('/simulation')
@admin_required
def simulation():
    user = get_current_user()
    return render_template('simulation.html', user=user)


@app.route('/settings')
@admin_required
def settings_page():
    """Admin settings page"""
    user = get_current_user()
    return render_template('settings.html', user=user)


# =========================
# ERROR HANDLING
# =========================

@app.errorhandler(401)
def unauthorized(e):
    """Unauthorized access - redirect to login"""
    return redirect(url_for('login'))


@app.errorhandler(403)
def forbidden(e):
    """Forbidden access - user doesn't have permission"""
    return render_template('unauthorized.html'), 403


@app.errorhandler(404)
def not_found(e):
    """Page not found"""
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Internal server error"""
    return "Something went wrong on the server", 500


# =========================
# RUN SERVER (DEPLOYMENT READY)
# =========================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # IMPORTANT for Railway/Render
    app.run(host='0.0.0.0', port=port)