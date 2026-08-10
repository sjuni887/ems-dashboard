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

calls_today = len(today_df)


# ====================================================
# AVERAGE CALLS PER DAY
# ====================================================

average_calls_per_day = (
    df.groupby(
        df["Date"].dt.date
    )
    .size()
    .mean()
)

average_calls_per_day = round(
    average_calls_per_day,
    1
)


# ====================================================
# DIFFERENCE FROM DAILY AVERAGE
# ====================================================

calls_difference = round(
    calls_today - average_calls_per_day
)


# ====================================================
# PATIENTS CONVEYED TODAY
# ====================================================

patients_conveyed_today = (
    today_df[
        "If not conveyed, what was the reason?"
    ]
    .fillna("")
    .str.strip()
    .eq("Not Applicable")
    .sum()
)


# ====================================================
# OTHER STATISTICS
# ====================================================

average_duration = round(
    df["Call Duration"].mean(),
    1
)

average_difficulty = round(
    df["How difficult was this call?"].mean(),
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
# Calls Today
# ----------------------------------------------------

with col1:

    st.metric(
        "Calls Today",
        calls_today
    )

    if calls_difference > 0:

        st.markdown(
            f"<small style='color:red;'>"
            f"▲ {calls_difference} above daily average"
            f"</small>",
            unsafe_allow_html=True
        )

    elif calls_difference < 0:

        st.markdown(
            f"<small style='color:green;'>"
            f"▼ {abs(calls_difference)} below daily average"
            f"</small>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            "<small>"
            "Exactly at daily average"
            "</small>",
            unsafe_allow_html=True
        )


# ----------------------------------------------------
# Patients Conveyed Today
# ----------------------------------------------------

with col2:

    st.metric(
        "Patients Conveyed Today",
        patients_conveyed_today
    )


# ----------------------------------------------------
# Average Duration
# ----------------------------------------------------

with col3:

    st.metric(
        "Average Duration",
        f"{average_duration} mins"
    )


# ----------------------------------------------------
# Average Difficulty
# ----------------------------------------------------

with col4:

    st.metric(
        "Average Difficulty",
        f"{average_difficulty}/5"
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
