import streamlit as st

from data.sheets import load_data
from data.cleaning import clean_data

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="EMS Dashboard",
    page_icon="🚑",
    layout="wide"
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

df = clean_data(load_data())

# ----------------------------------------------------
# Statistics
# ----------------------------------------------------

total_calls = len(df)

average_age = round(df["Patient Age"].mean(), 1)

average_duration = round(df["Call Duration"].mean(), 1)

average_difficulty = round(df["How difficult was this call?"].mean(), 1)

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("🚑 EMS Dashboard")
st.caption("Personal EMS Call Analytics Dashboard")

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Calls", total_calls)

with col2:
    st.metric("Average Patient Age", average_age)

with col3:
    st.metric("Average Duration", f"{average_duration} mins")

with col4:
    st.metric("Average Difficulty", f"{average_difficulty}/5")

st.divider()

# ----------------------------------------------------
# Recent Calls
# ----------------------------------------------------

st.subheader("📋 Recent Calls")

recent_calls = (
    df[
        [
            "Date",
            "Call start time",
            "Call Type",
            "Starting PAC status",
            "Ending PAC Status",
            "Patient Age",
            "Call Duration",
        ]
    ]
    .sort_values("Date", ascending=False)
)

st.dataframe(
    recent_calls,
    use_container_width=True,
    hide_index=True,
)