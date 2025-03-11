import streamlit as st
from database import init_db, save_user, check_credentials, get_user_email, get_member_since
from healthcare_data import load_healthcare_data
from visualization import plot_scatter, plot_bar, plot_line, plot_histogram, plot_boxplot, plot_heatmap, generate_pdf_report, generate_best_viz
import pandas as pd
import io

def main():
    st.set_page_config(
        page_title="Datavista",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        st.title("Welcome to Datavista!")
        st.markdown("Please login or sign up to continue")
        auth_choice = st.radio("Select Option", ["Login", "Sign Up"], index=0)

        if auth_choice == "Login":
            st.subheader("Login to Your Account")
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
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
        else:
            st.subheader("Create a New Account")
            cols = st.columns([1, 2, 1])
            with cols[1]:
                with st.form(key="signup_form"):
                    new_username = st.text_input("Choose a Username")
                    new_email = st.text_input("Enter your Email")
                    new_password = st.text_input("Choose a Password", type="password")
                    submit_signup = st.form_submit_button("Sign Up")
                if submit_signup:
                    if new_username == "" or new_password == "" or new_email == "":
                        st.error("Please enter a username, email, and password!")
                    elif save_user(new_username, new_password, new_email):
                        st.success("User created successfully! Please log in.")
                        st.rerun()
                    else:
                        st.error("Username already exists!")
        return

    st.sidebar.title("Datavista")
    page = st.sidebar.radio("Go to", ["Dashboard", "Upload Dataset", "Profile", "Download Report"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.title("DataVista: A Simplified Data Visualization Approach")
    st.markdown(f"**Welcome, {st.session_state.username}!**")
    st.markdown(f"*Today is {pd.to_datetime('today').strftime('%a, %b %d, %Y')}*")

    df = load_healthcare_data()

    if page == "Dashboard":
        st.header("Dashboard")
        st.markdown("### Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(plot_scatter(df))
            st.pyplot(plot_histogram(df))
        with col2:
            st.pyplot(plot_bar(df))
            st.pyplot(plot_boxplot(df))
        st.pyplot(plot_line(df))
        st.pyplot(plot_heatmap(df))
    elif page == "Upload Dataset":
        st.header("Upload Your Dataset")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            df_uploaded = pd.read_csv(uploaded_file)
            st.write("### Preview of Uploaded Data")
            st.write(df_uploaded.head())
            
            st.write("### Suggested Visualizations")
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(plot_scatter(df_uploaded))
                st.pyplot(plot_histogram(df_uploaded))
            with col2:
                st.pyplot(plot_bar(df_uploaded))
                st.pyplot(plot_boxplot(df_uploaded))
            st.pyplot(plot_line(df_uploaded))
            st.pyplot(plot_heatmap(df_uploaded))
            
            # Additional Download Report Feature
            st.write("### Download Report for Uploaded Data")
            pdf_uploaded_buffer = generate_pdf_report(df_uploaded)
            st.download_button(
                label="Download PDF Report for Uploaded Data",
                data=pdf_uploaded_buffer,
                file_name="uploaded_data_report.pdf",
                mime="application/pdf"
            )
    elif page == "Profile":
        st.header("Profile")
        st.markdown("### Account Details")
        st.write(f"**Username:** {st.session_state.username}")
        user_email = get_user_email(st.session_state.username)
        st.write(f"**Email:** {user_email}")
        member_since = get_member_since(st.session_state.username)
        st.write(f"**Member Since:** {member_since}")
    elif page == "Download Report":
        st.header("Download Report")
        pdf_buffer = generate_pdf_report(df)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="healthcare_report.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
