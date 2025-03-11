import streamlit as st
import base64
import pandas as pd
from database import init_db, save_user, check_credentials, get_user_email, get_member_since, change_password
from healthcare_data import load_healthcare_data
from visualization import plot_scatter, plot_bar, plot_line, plot_histogram, plot_boxplot, plot_heatmap, generate_pdf_report, generate_best_viz

def add_bg_from_local(image_file):
    """
    Reads a local image file, encodes it in base64,
    and injects CSS to set it as the background.
    """
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="Datavista",
        page_icon=":chart_with_upwards_trend:",
        layout="wide"
    )

    # Custom CSS for sidebar and login/sign-up pages
    st.markdown(
        """
        <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #71b7e6, #9b59b6);
            color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        [data-testid="stSidebar"] .sidebar-content {
            padding: 20px;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p {
            color: black;
        }
        /* Custom CSS for Login and Sign Up pages */
        h1, h2, h3 {
            color: #333;
        }
        .stRadio > div {
            display: flex;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        [data-testid="stForm"] {
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTextInput>div>input {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 0.5rem;
        }
        .stButton button {
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )

    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # Apply background image only for login/sign-up page
    if not st.session_state.logged_in:
        add_bg_from_local("background.png")
        st.markdown("<div style='text-align: center;'><h1>Welcome to Datavista!</h1></div>", unsafe_allow_html=True)
        auth_choice = st.radio(
            "Select Option", ["Login", "Sign Up"], index=0, horizontal=True, label_visibility="hidden"
        )

        if auth_choice == "Login":
            st.markdown("<div style='text-align: center;'><h3>Login to Your Account</h3></div>", unsafe_allow_html=True)
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
            st.markdown("<div style='text-align: center;'><h3>Create a New Account</h3></div>", unsafe_allow_html=True)
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
                        st.session_state.logged_in = True
                        st.session_state.username = new_username
                        st.success("User created successfully and logged in!")
                        st.rerun()
                    else:
                        st.error("Username already exists!")
        return

    # Main app (post login)
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

        st.markdown("### Change Password")
        col_left, col_right = st.columns([1, 1])
        with col_left:
            with st.form(key="change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                submit_change = st.form_submit_button("Change Password")
        if submit_change:
            if new_password != confirm_password:
                st.error("New password and confirmation do not match!")
            elif change_password(st.session_state.username, current_password, new_password):
                st.success("Password changed successfully!")
            else:
                st.error("Current password is incorrect!")
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
