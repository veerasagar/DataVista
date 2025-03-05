import streamlit as st
from database import init_db, save_user, check_credentials
from healthcare_data import load_healthcare_data
from visualization import plot_scatter, plot_bar, plot_line, generate_pdf_report
import pandas as pd

def main():
    st.set_page_config(page_title="Datavista", layout="wide")
    init_db()  # Ensure the database is initialized

    # Initialize session state for authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # --- Login / Sign Up Section ---
    if not st.session_state.logged_in:
        st.title("Welcome to the Datavista!!!")
        st.markdown("Please login or sign up to continue")
        auth_choice = st.radio("Select Option", ["Login", "Sign Up"], index=0, key="auth_choice")

        if auth_choice == "Login":
            st.subheader("Login to Your Account")
            # Center the login form using columns
            cols = st.columns([1, 2, 1])
            with cols[1]:
                with st.form(key="login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submit_login = st.form_submit_button("Login")
                if submit_login:
                    if check_credentials(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Logged in successfully!")
                        st.rerun()  # Rerun the app to load the dashboard
                    else:
                        st.error("Invalid username or password!")
        else:
            st.subheader("Create a New Account")
            # Center the sign-up form using columns
            cols = st.columns([1, 2, 1])
            with cols[1]:
                with st.form(key="signup_form"):
                    new_username = st.text_input("Choose a Username")
                    new_password = st.text_input("Choose a Password", type="password")
                    submit_signup = st.form_submit_button("Sign Up")
                if submit_signup:
                    if new_username == "" or new_password == "":
                        st.error("Please enter a username and password!")
                    elif save_user(new_username, new_password):
                        st.success("User created successfully! Please log in.")
                        st.rerun()
                    else:
                        st.error("Username already exists!")
        return  # Stop here if not logged in

    # --- Main Dashboard Section (after login) ---
    st.sidebar.title("Datavista!")
    page = st.sidebar.radio("Go to", ["Dashboard", "Profile", "Download Report"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.title("DataVista: A Simplified Data Visualization Approach")
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
