import streamlit as st
from google.oauth2 import service_account
import gspread

import pandas as pd

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
gc = gspread.authorize(credentials)
gsheets_url = st.secrets["private_gsheets"]["private_gsheets_url"]
spreadsheet = gc.open_by_url(gsheets_url)


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # select spreadsheet, then sheet
        worksheet = spreadsheet.worksheet("Passwords")
        list_of_dicts = worksheet.get_all_records()
        df = pd.DataFrame(list_of_dicts)

        if (
                st.session_state["username"] in df['username'].values
                and ((df['username'] == st.session_state["username"]) &
                     (df['password'] == st.session_state["password"])).any()
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


if check_password():
    st.write("Here goes your normal Streamlit app...")

# Retrieve sheet names
spreadsheet = gc.open_by_url(gsheets_url)
sheet_names = [s.title for s in spreadsheet.worksheets()]
erg_sheet_names = [title for title in sheet_names if "🔐" not in title]
st.write(erg_sheet_names)
