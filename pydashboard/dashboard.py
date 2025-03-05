from flask import Blueprint, render_template, session, redirect, url_for, send_file
import matplotlib.pyplot as plt
import io
import base64
from data_loader import load_healthcare_data
from matplotlib.backends.backend_pdf import PdfPages

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    df = load_healthcare_data()
    
    # Visualization 1: Scatter plot - Age vs. Cholesterol
    plt.figure(figsize=(8,6))
    plt.scatter(df['Age'], df['Cholesterol'], c='blue', label='Patients')
    plt.title('Age vs. Cholesterol')
    plt.xlabel('Age')
    plt.ylabel('Cholesterol')
    plt.grid(True)
    plt.legend()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    scatter_img = base64.b64encode(buf1.getvalue()).decode('utf8')
    plt.close()
    
    # Visualization 2: Bar chart - Heart Disease Count
    plt.figure(figsize=(8,6))
    heart_counts = df['HeartDisease'].value_counts()
    plt.bar(heart_counts.index, heart_counts.values, color=['green', 'red'])
    plt.title('Heart Disease Count')
    plt.xlabel('Heart Disease')
    plt.ylabel('Number of Patients')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    bar_img = base64.b64encode(buf2.getvalue()).decode('utf8')
    plt.close()
    
    # Visualization 3: Line plot - Age vs. BMI
    plt.figure(figsize=(8,6))
    plt.plot(df['Age'], df['BMI'], marker='o', linestyle='-', color='orange')
    plt.title('Age vs. BMI')
    plt.xlabel('Age')
    plt.ylabel('BMI')
    plt.grid(True)
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    line_img = base64.b64encode(buf3.getvalue()).decode('utf8')
    plt.close()
    
    return render_template(
        'dashboard.html', 
        username=session['user'], 
        scatter_img=scatter_img, 
        bar_img=bar_img,
        line_img=line_img
    )

@dashboard_bp.route('/download_report')
def download_report():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    df = load_healthcare_data()
    
    # Create a PDF report with the visualizations
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        # Visualization 1: Scatter plot - Age vs. Cholesterol
        fig1 = plt.figure(figsize=(8,6))
        plt.scatter(df['Age'], df['Cholesterol'], c='blue', label='Patients')
        plt.title('Age vs. Cholesterol')
        plt.xlabel('Age')
        plt.ylabel('Cholesterol')
        plt.grid(True)
        plt.legend()
        pdf.savefig(fig1)
        plt.close(fig1)
        
        # Visualization 2: Bar chart - Heart Disease Count
        fig2 = plt.figure(figsize=(8,6))
        heart_counts = df['HeartDisease'].value_counts()
        plt.bar(heart_counts.index, heart_counts.values, color=['green', 'red'])
        plt.title('Heart Disease Count')
        plt.xlabel('Heart Disease')
        plt.ylabel('Number of Patients')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        pdf.savefig(fig2)
        plt.close(fig2)
        
        # Visualization 3: Line plot - Age vs. BMI
        fig3 = plt.figure(figsize=(8,6))
        plt.plot(df['Age'], df['BMI'], marker='o', linestyle='-', color='orange')
        plt.title('Age vs. BMI')
        plt.xlabel('Age')
        plt.ylabel('BMI')
        plt.grid(True)
        pdf.savefig(fig3)
        plt.close(fig3)
    
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer, 
        as_attachment=True, 
        download_name='healthcare_report.pdf', 
        mimetype='application/pdf'
    )

@dashboard_bp.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', username=session['user'])
