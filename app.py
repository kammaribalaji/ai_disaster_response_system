from flask import Flask, render_template
import os

from routes.predict import predict_bp
from routes.map import map_bp
from routes.route_opt import route_bp
from routes.dashboard import dashboard_bp
from routes.report import report_bp
from routes.relief import relief_bp
from routes.chat import chat_bp
from routes.tasks import tasks_bp
from database.db import init_db

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'assets'),
            static_url_path='/assets')

# Initialize SQLite tables before serving requests
init_db()

app.register_blueprint(predict_bp)
app.register_blueprint(map_bp)
app.register_blueprint(route_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(relief_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(tasks_bp)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/rescue-dashboard')
def rescue_dashboard():
    return render_template('rescue_dashboard.html')

@app.route('/public-dashboard')
def public_dashboard():
    return render_template('public_dashboard.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/routes')
def routes():
    return render_template('routes.html')

@app.route('/relief')
def relief():
    return render_template('relief.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
