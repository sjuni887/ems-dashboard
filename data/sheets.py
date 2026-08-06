import streamlit as st
import pandas as pd

@st.cache_data(ttl=60)
def load_data():
    # Spreadsheet ID
    gsheetkey = "1AjNfVRE5ejv4dB7Usq2FE1TbJooEBMlykguLvKjKJZw"

    # Worksheet name
    sheet_name = "Form responses 1"

    # Export as Excel
    url = f"https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx"

    # Read into DataFrame
    df = pd.read_excel(url, sheet_name=sheet_name)

    return df