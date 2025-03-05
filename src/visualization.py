# visualization.py
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_pdf import PdfPages

def plot_scatter(df):
    """Create a scatter plot of Age vs. Cholesterol."""
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(df['Age'], df['Cholesterol'], color='blue', label='Patients')
    ax.set_title('Age vs. Cholesterol')
    ax.set_xlabel('Age')
    ax.set_ylabel('Cholesterol')
    ax.grid(True)
    ax.legend()
    return fig

def plot_bar(df):
    """Create a bar chart for the Heart Disease count."""
    fig, ax = plt.subplots(figsize=(8,6))
    heart_counts = df['HeartDisease'].value_counts()
    ax.bar(heart_counts.index, heart_counts.values, color=['green', 'red'])
    ax.set_title('Heart Disease Count')
    ax.set_xlabel('Heart Disease')
    ax.set_ylabel('Number of Patients')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

def plot_line(df):
    """Create a line plot of Age vs. BMI."""
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(df['Age'], df['BMI'], marker='o', linestyle='-', color='orange')
    ax.set_title('Age vs. BMI')
    ax.set_xlabel('Age')
    ax.set_ylabel('BMI')
    ax.grid(True)
    return fig

def generate_pdf_report(df):
    """Generates a multi-page PDF report containing the three visualizations."""
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        fig1 = plot_scatter(df)
        pdf.savefig(fig1)
        plt.close(fig1)
        fig2 = plot_bar(df)
        pdf.savefig(fig2)
        plt.close(fig2)
        fig3 = plot_line(df)
        pdf.savefig(fig3)
        plt.close(fig3)
    pdf_buffer.seek(0)
    return pdf_buffer