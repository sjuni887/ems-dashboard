import streamlit as st

from data.sheets import load_data
from data.cleaning import clean_data


# ====================================================
# LOAD DATA
# ====================================================

df = clean_data(load_data())


# ====================================================
# PAGE TITLE
# ====================================================

st.title("📋 Raw Data")

st.caption(
    "view all data"
)


# ====================================================
# FILTERS
# ====================================================

st.sidebar.header("Filters")


# ----------------------------------------------------
# Date Filter
# ----------------------------------------------------

dates = sorted(
    df["Date"]
    .dropna()
    .unique()
)

selected_dates = st.sidebar.multiselect(
    "Date",
    options=dates,
    default=dates
)


# ----------------------------------------------------
# Shift Filter
# ----------------------------------------------------

shift_options = sorted(
    df["Shift"]
    .dropna()
    .unique()
)

selected_shifts = st.sidebar.multiselect(
    "Shift",
    options=shift_options,
    default=shift_options
)


# ----------------------------------------------------
# Call Type Filter
# ----------------------------------------------------

call_type_options = sorted(
    df["Call Type"]
    .dropna()
    .unique()
)

selected_call_types = st.sidebar.multiselect(
    "Call Type",
    options=call_type_options,
    default=call_type_options
)


# ----------------------------------------------------
# Starting PAC Filter
# ----------------------------------------------------

pac_options = sorted(
    df["Starting PAC status"]
    .dropna()
    .unique()
)

selected_pac = st.sidebar.multiselect(
    "Starting PAC",
    options=pac_options,
    default=pac_options
)


# ----------------------------------------------------
# Ending PAC Filter
# ----------------------------------------------------

ending_pac_options = sorted(
    df["Ending PAC Status"]
    .dropna()
    .unique()
)

selected_ending_pac = st.sidebar.multiselect(
    "Ending PAC",
    options=ending_pac_options,
    default=ending_pac_options
)


# ----------------------------------------------------
# Gender Filter
# ----------------------------------------------------

gender_options = sorted(
    df["Patient Gender"]
    .dropna()
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Patient Gender",
    options=gender_options,
    default=gender_options
)


# ----------------------------------------------------
# Difficulty Filter
# ----------------------------------------------------

difficulty_options = sorted(
    df["How difficult was this call?"]
    .dropna()
    .unique()
)

selected_difficulty = st.sidebar.multiselect(
    "Difficulty",
    options=difficulty_options,
    default=difficulty_options
)


# ====================================================
# APPLY FILTERS
# ====================================================

filtered_df = df[
    df["Date"].isin(selected_dates)
    & df["Shift"].isin(selected_shifts)
    & df["Call Type"].isin(selected_call_types)
    & df["Starting PAC status"].isin(selected_pac)
    & df["Ending PAC Status"].isin(selected_ending_pac)
    & df["Patient Gender"].isin(selected_gender)
    & df["How difficult was this call?"].isin(selected_difficulty)
].copy()


# ====================================================
# SUMMARY
# ====================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Calls Shown",
        len(filtered_df)
    )

with col2:

    st.metric(
        "Total Calls",
        len(df)
    )


st.divider()


# ====================================================
# DATA TABLE
# ====================================================

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

