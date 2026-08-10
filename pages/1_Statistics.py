import streamlit as st

from data.sheets import load_data
from data.cleaning import clean_data

from components.call_analytics import show_call_analytics
from components.patient_analytics import show_patient_analytics
from components.pac_analytics import show_pac_analytics
from components.operations_analytics import show_operations_analytics

st.set_page_config(
    page_title="EMS Statistics",
    page_icon="📊",
    layout="wide"
)

df = clean_data(load_data())

st.title("📊 EMS Statistics")
st.caption("noob statistics")

show_call_analytics(df)

st.divider()

show_patient_analytics(df)

st.divider()

show_pac_analytics(df)

st.divider()

show_operations_analytics(df)