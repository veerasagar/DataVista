from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User, fs, db
import os
from dotenv import load_dotenv
import pandas as pd
import openai
import uuid
import plotly
import json
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}

openai.api_key = os.getenv("OPENAI_API_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_visualization(df):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": f"Generate Plotly Express Python code to visualize this healthcare data. Data sample: {df.head(2).to_dict()}. Create 3 different visualizations. Return only valid Python code."
            }]
        )
        code = response.choices[0].message.content
        return safe_execute_code(code, df)
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return []

def safe_execute_code(code, df):
    allowed_imports = {
        'plotly.express': ['px'],
        'pandas': ['pd']
    }
    
    local_vars = {'df': df, 'px': None, 'pd': pd}
    global_vars = {}
    
    try:
        exec(code, global_vars, local_vars)
        figs = [v for v in local_vars.values() if isinstance(v, plotly.graph_objs.Figure)]
        return figs[:3]
    except Exception as e:
        print(f"Execution Error: {str(e)}")
        return []

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)
        
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.get(username):
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        new_user = User(username, email, password)
        new_user.save()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())
            
            # Read and process file
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Generate visualizations
            figures = generate_visualization(df)
            if not figures:
                flash('Failed to generate visualizations')
                return redirect(url_for('dashboard'))
            
            # Store visualizations
            viz_data = []
            for i, fig in enumerate(figures):
                viz_id = f"{file_id}_{i}"
                viz_json = json.loads(fig.to_json())
                db.visualizations.insert_one({
                    'viz_id': viz_id,
                    'user': current_user.id,
                    'data': viz_json
                })
                viz_data.append(viz_id)
            
            return render_template('dashboard.html', 
                                username=current_user.id,
                                visualizations=viz_data)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('dashboard'))
    
    flash('Invalid file type')
    return redirect(url_for('dashboard'))

@app.route('/viz/<viz_id>')
@login_required
def get_visualization(viz_id):
    viz_data = db.visualizations.find_one({'viz_id': viz_id, 'user': current_user.id})
    if not viz_data:
        return "Visualization not found", 404
    
    fig = plotly.io.from_json(json.dumps(viz_data['data']))
    return fig.to_html(full_html=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)