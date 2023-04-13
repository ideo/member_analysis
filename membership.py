import streamlit as st
import altair as alt

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
    raw_emails = st.text_area('Add emails from slack channel to fill charts', '''''')
    member_emails = raw_emails.split(", ")
    member_emails = [x.strip() for x in member_emails]
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
    df = df[df['Worker'] != 'Expensify User'].copy()

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


def check_for_non_ideo_com_members(member_emails, employee_df):
    ideo_email_list = employee_df[email_col].unique().tolist()
    outside_ideo_com = list(set(member_emails) - set(ideo_email_list))
    if outside_ideo_com:
        if outside_ideo_com != [""]:
            email_cnt = len(outside_ideo_com)
        else:
            email_cnt = 0
        st.header(f'ERG members without ideo.com email address OR not in Workday data: {email_cnt}')
        my_expander = st.expander(label='Expand me to see emails')
        with my_expander:
            st.write(outside_ideo_com)


def extract_member_data(employee_df, member_emails):
    member_data_df = employee_df[employee_df[email_col].isin(member_emails)].copy()
    member_data_df.reset_index(inplace=True, drop=True)
    check_for_non_ideo_com_members(member_emails, member_data_df)

    return member_data_df


def fill_chart(df, x, y, xbin=False, ysort=None, tooltip=None):
    if tooltip:
        return (
            alt.Chart(df)
            .mark_bar()
            .encode(
                alt.X(x, bin=xbin),
                alt.Y(y, sort=ysort),
                alt.Color("level_group", sort=power, scale=alt.Scale(scheme='magma')),
                tooltip=tooltip
            )
            .interactive()
        )
    else:
        return (
            alt.Chart(df)
            .mark_bar()
            .encode(
                alt.X(x, bin=xbin),
                alt.Y(y, sort=ysort),
                alt.Color("level_group", sort=power, scale=alt.Scale(scheme='magma')),
            )
            .interactive()
        )


def plot_general_info(erg_df):
    st.title('General Employee Data')
    st.caption('Source: Workday March 2023 - Contains some errors')
    st.subheader(f'Raw IDEO.com Employee Data: {erg_df.shape[0]}')
    st.dataframe(erg_df)

    col1, col2 = st.columns([3, 2])
    streamlit_cols = [col1, col2, col2]

    for i, col in enumerate(general_section):
        with streamlit_cols[i]:
            # COUNTS BY CATEGORY
            group_sizes = erg_df.groupby(col).size().reset_index(name='count')
            # if group_sizes.shape[0] > 1:
            # TITLE & DATA
            st.subheader(col)
            my_expander = st.expander(label='Expand me')
            with my_expander:
                st.dataframe(group_sizes)
            # PLOT
            x = "count()"
            y = f"{col}:O"
            ysort = '-x'
            tooltip = ["Worker", "cost_center_type", cost_center_col, level_col,
                       alt.Tooltip('tenure_in_yrs:Q', format=",.2f"), "Location"]
            chart = fill_chart(erg_df, x=x, y=y, ysort=ysort, tooltip=tooltip)
            st.altair_chart(chart)


def remove_contingency_option(erg_df, section):
    types = erg_df['Worker Type'].unique()
    df = erg_df.copy()
    if "Contingent Worker" in types:
        exclude_contingency = st.radio(
            "Exclude Contingency Workers?",
            ('No', 'Yes'),
            key=section
        )

        if exclude_contingency == "Yes":
            df = erg_df[erg_df['Worker Type'] != 'Contingent Worker'].copy()
    return df


def plot_level_info(erg_df):
    st.title('Power distribution')
    df = remove_contingency_option(erg_df, section="level")

    for col in level_section:
        col1, col2 = st.columns([3, 2])
        with col1:
            if col == 'tenure_in_yrs':
                x = f"{col}:Q"
                y = "count()"
                chart = fill_chart(df, x=x, y=y, xbin=True)
                # plot_ridge_line(erg_df)
            else:
                if col == 'level_group':
                    x = "count()"
                    y = f"{col}:O"
                    chart = fill_chart(df, x=x, y=y, ysort=management_levels)

                else:
                    x = "count()"
                    y = f"{col}:O"
                    tooltip = ["Worker", "cost_center_type", cost_center_col, level_col,
                               alt.Tooltip('tenure_in_yrs:Q', format=",.2f"), "Location"]
                    chart = fill_chart(df, x=x, y=y, ysort=management_levels, tooltip=tooltip)

            st.subheader(col)
            st.altair_chart(chart)
        with col2:
            if col == 'tenure_in_yrs':
                df[col] = df[col].round()

            group_sizes = df.groupby(col).size().reset_index(name='count')
            st.dataframe(group_sizes)


def plot_location_info(erg_df):
    st.title("Where is everyone?")
    df = remove_contingency_option(erg_df, section="Location")

    for col in location_section:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader(col)
            x = "count()"
            y = f"{col}:O"
            ysort = '-x'
            chart = fill_chart(df, x=x, y=y, ysort=ysort)
            st.altair_chart(chart)
        with col2:
            group_sizes = df.groupby(col).size().reset_index(name='count')
            st.dataframe(group_sizes)


def plot_data(erg_df):
    plot_general_info(erg_df)
    plot_level_info(erg_df)
    plot_location_info(erg_df)


if check_password():
    st.title("Ask more informed questions!")
    st.write("TKTK - Msg to users & disclaimer about what's in and not in data")
    # Retrieve sheet names

    erg_member_emails = load_member_emails()
    employee_data_df = load_employee_data()
    erg_member_data_df = extract_member_data(employee_data_df, erg_member_emails)

    plot_data(erg_member_data_df)
