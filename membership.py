import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd
import datetime
import numpy as np

from settings import *

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
        worksheet = spreadsheet.worksheet("🔐 Passwords")
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


def load_member_emails():
    raw_emails = st.text_area('Add emails from slack channel', '''''')
    member_emails = raw_emails.split(", ")
    member_cnt = 0
    if raw_emails:
        member_cnt = len(member_emails)

    st.caption(f'Number of member emails loaded: {member_cnt}')
    return member_emails


def load_raw_employee_data():
    worksheet = spreadsheet.worksheet("🔐 Workday employee data 04.2023")
    list_of_dicts = worksheet.get_all_records()
    df = pd.DataFrame(list_of_dicts)

    df = df[df['Active Status'] == 1].copy()

    sub_cols = []
    sub_cols.extend(identifiers)
    sub_cols.extend(biz_details)
    return df[sub_cols].copy()


def add_true_regions(df):
    for k, v in true_region_mapping.items():
        df.loc[df['Location'].str.contains('|'.join(v)), 'region_simplified'] = k

    return df


def clean_studio_names(df):
    df['studio'] = df['Location']
    df.loc[df['Location'].str.contains('Remote|Cloud'), 'studio'] = 'Cloud'
    for studio in studio_details:
        df.loc[df['Location'].str.contains(studio), 'studio'] = studio

    return df


def clean_geographic_data(df):
    df = clean_studio_names(df)
    df = add_true_regions(df)

    return df


def add_level_groups(df):
    # 2 enterprise individuals NA - this is rough fix
    df[level_col].fillna('Senior Enterprise', inplace=True)

    df['level_group'] = df[level_col]

    df.loc[df[level_col].str.contains('Individual', na=False), 'level_group'] = 'Individual'
    df.loc[df[level_col].str.contains('Team', na=False), 'level_group'] = 'Team'
    df.loc[df[level_col].str.contains('Director', na=False), 'level_group'] = 'Director'
    df.loc[df[level_col].str.contains('Enterprise', na=False), 'level_group'] = 'Enterprise'

    return df

def add_cost_center_type(df):

    df['cost_center_type'] = df[cost_center_col]

    for job_family in internal_cost_centers:
        df.loc[df[cost_center_col].str.contains(job_family), 'cost_center_type'] = 'Internal'

    df.loc[df[cost_center_col].str.contains('General'), 'cost_center_type'] = 'External'
    df.loc[df[cost_center_col].str.contains('IDEO U'), 'cost_center_type'] = 'External'
    df.loc[df[cost_center_col].str.contains('Open Financial Systems'), 'cost_center_type'] = 'External'
    df.loc[df[cost_center_col].str.contains('Shop'), 'cost_center_type'] = 'External'
    df.loc[df[cost_center_col].str.contains('Production'), 'cost_center_type'] = 'External'
    df.loc[df[cost_center_col].str.contains('Creative Leadership'), 'cost_center_type'] = 'External'

    return df


def add_ideo_tenure(df):
    df['Hire Date'] = pd.to_datetime(df['Hire Date'])
    df['tenure_in_yrs'] = (datetime.datetime.now() - df['Hire Date']) / np.timedelta64(1, 'Y')
    return df


def load_employee_data():
    df = load_raw_employee_data()
    df = clean_geographic_data(df)
    df = add_level_groups(df)
    df = add_cost_center_type(df)
    return add_ideo_tenure(df)


def extract_member_data(employee_df, member_emails):
    member_data_df = employee_df[employee_df[email_col].isin(member_emails)].copy()
    member_data_df.reset_index(inplace=True, drop=True)
    # check_for_non_ideo_com_members(member_emails, erg_member_data_df)

    return member_data_df


if check_password():
    st.title("Ask more informed questions!")
    st.header("TKTK - Msg to users & disclaimer about what's in and not in data")
    # Retrieve sheet names

    erg_member_emails = load_member_emails()
    employee_data_df = load_employee_data()
    erg_member_data_df = extract_member_data(employee_data_df, erg_member_emails)
