import streamlit as st

from data.sheets import load_data
from data.cleaning import clean_data


# ====================================================
# LOAD DATA
# ====================================================

df = clean_data(load_data())


# ====================================================
# STATISTICS
# ====================================================

total_calls = len(df)

average_age = round(
    df["Patient Age"].mean(),
    1
)

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


with col1:

    st.metric(
        "Total Calls",
        total_calls
    )


with col2:

    st.metric(
        "Average Patient Age",
        average_age
    )


with col3:

    st.metric(
        "Average Duration",
        f"{average_duration} mins"
    )


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