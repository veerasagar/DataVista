import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_pdf import PdfPages
import os

# -----------------------------
# Database Functions for User Authentication
# -----------------------------
DATABASE = "users.db"

def init_db():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user(username, password):
    """Saves a new user to the database. Returns True if successful, False if the username exists."""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_credentials(username, password):
    """Checks if the given username and password match a record in the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# -----------------------------
# Healthcare Data and Visualization Functions
# -----------------------------
def load_healthcare_data():
    """Load healthcare data from a CSV file if it exists; otherwise, create a sample dataset."""
    DATASET_FILE = "healthcare_data.csv"
    if os.path.exists(DATASET_FILE):
        df = pd.read_csv(DATASET_FILE)
    else:
        data = {
            "PatientID": [1,2,3,4,5,6,7,8,9,10],
            "Age": [45,50,39,60,55,40,65,70,30,50],
            "BMI": [28.5,30.2,24.8,32.0,29.5,27.0,31.0,33.5,22.5,28.0],
            "BloodPressure": [130,135,120,140,132,125,145,150,115,130],
            "Cholesterol": [220,240,200,260,230,210,250,270,190,220],
            "HeartDisease": ["Yes", "No", "No", "Yes", "Yes", "No", "Yes", "Yes", "No", "No"]
        }
        df = pd.DataFrame(data)
    return df

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

# -----------------------------
# Main Streamlit Application
# -----------------------------
def main():
    st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
    init_db()  # Ensure the database is initialized

    # Initialize session state for authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # --- Login / Sign Up Section ---
    if not st.session_state.logged_in:
        st.title("Welcome to the Healthcare Dashboard")
        auth_choice = st.radio("Select Option", ["Login", "Sign Up"])
        if auth_choice == "Login":
            st.header("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if check_credentials(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    if hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
                    else:
                        st.stop()
                else:
                    st.error("Invalid username or password!")
        else:
            st.header("Sign Up")
            new_username = st.text_input("Choose a Username", key="signup_username")
            new_password = st.text_input("Choose a Password", type="password", key="signup_password")
            if st.button("Sign Up"):
                if new_username == "" or new_password == "":
                    st.error("Please enter a username and password!")
                elif save_user(new_username, new_password):
                    st.success("User created successfully! Please log in.")
                    if hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
                    else:
                        st.stop()
                else:
                    st.error("Username already exists!")
        return  # Stop here if not logged in

    # --- Main Dashboard Section (after login) ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Profile", "Download Report"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()

    st.title("Healthcare Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!**")
    st.markdown(f"*Today is {pd.to_datetime('today').strftime('%a, %b %d, %Y')}*")

    # Load healthcare data
    df = load_healthcare_data()

    if page == "Dashboard":
        st.header("Dashboard")
        st.markdown("### Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(plot_scatter(df))
        with col2:
            st.pyplot(plot_bar(df))
        st.pyplot(plot_line(df))
    elif page == "Profile":
        st.header("Profile")
        st.markdown("### Account Details")
        st.write(f"**Username:** {st.session_state.username}")
        st.write("**Email:** user@example.com")
        st.write("**Member Since:** January 1, 2022")
        st.markdown("### Activity Summary")
        st.write("You have logged in 5 times.")
        st.write("Last login: Today")
        st.markdown("### Reports")
        st.write("You have generated 3 reports.")
        if st.button("Edit Profile"):
            st.info("Profile edit functionality coming soon!")
    elif page == "Download Report":
        st.header("Download Report")
        st.markdown("Click the button below to download your healthcare report as a PDF.")
        pdf_buffer = generate_pdf_report(df)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="healthcare_report.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
