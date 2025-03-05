from flask import Flask, redirect, url_for
from database import init_db
from auth import auth_bp
from dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key in production

# Initialize the database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
