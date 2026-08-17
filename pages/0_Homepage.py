import streamlit as st
import pandas as pd

from data.sheets import load_data
from data.cleaning import clean_data


# ====================================================
# LOAD DATA
# ====================================================

df = clean_data(load_data())


# ====================================================
# DATE PREPARATION
# ====================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()


# ====================================================
# TODAY'S CALLS
# ====================================================

today_df = df[
    df["Date"].dt.normalize() == today
].copy()

# ====================================================
# CALLS THIS SHIFT
# ====================================================

calls_this_shift = len(today_df)


# ====================================================
# CURRENT SHIFT
# ====================================================

if len(today_df) > 0:

    # Sort by date so the most recent call is last
    today_df = today_df.sort_values(
        "Date"
    )

    current_shift = today_df.iloc[-1]["Shift"]

else:

    current_shift = "—"


# ====================================================
# PATIENTS CONVEYED
# ====================================================

patients_conveyed = (
    today_df[
        "If not conveyed, what was the reason?"
    ]
    .fillna("")
    .str.strip()
    .eq("Not Applicable")
    .sum()
)


# ====================================================
# AVERAGE DURATION
# ====================================================

average_duration = round(
    df["Call Duration"].mean(),
    1
)


# ====================================================
# TITLE
# ====================================================

st.title("EMS Dashboard")

st.caption(
    "personal ems call dashboard - station 44"
)


# ====================================================
# SUMMARY
# ====================================================

col1, col2, col3, col4 = st.columns(4)


# ----------------------------------------------------
# Calls This Shift
# ----------------------------------------------------

with col1:

    st.metric(
        "Calls This Shift",
        calls_this_shift
    )


# ----------------------------------------------------
# Shift
# ----------------------------------------------------

with col2:

    st.metric(
        "Shift",
        current_shift
    )


# ----------------------------------------------------
# Patients Conveyed
# ----------------------------------------------------

with col3:

    st.metric(
        "Patients Conveyed",
        patients_conveyed
    )


# ----------------------------------------------------
# Average Duration
# ----------------------------------------------------

with col4:

    st.metric(
        "Average Duration",
        f"{average_duration} mins"
    )


st.divider()


# ====================================================
# RECENT CALLS
# ====================================================

st.subheader("📋 Recent Calls")


recent_calls = (
    df[
        [
            "Date",
            "Alpha/ Callsign",
            "Shift",
            "Call start time",
            "Call Type",
            "Starting PAC status",
            "Ending PAC Status",
            "Patient Age",
            "Call Duration",
        ]
    ]
    .sort_values(
        "Date",
        ascending=False
    )
    .head(10)
)


st.dataframe(
    recent_calls,
    use_container_width=True,
    hide_index=True
)