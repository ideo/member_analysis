import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

import pandas as pd


# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        users_url = st.secrets["private_gsheets"]["private_gsheets_url_passwords"]
        rows = run_query(f'SELECT * FROM "{users_url}"')
        df = pd.DataFrame(rows)

        if (
                st.session_state["username"] in df['username'].values
                and ((df['username'] == st.session_state["username"]) & (
                df['password'] == st.session_state["password"])).any()
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

if check_password():
    st.write("Here goes your normal Streamlit app...")
