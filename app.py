import streamlit as st


# ====================================================
# PAGE CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="EMS Dashboard",
    page_icon="🚑",
    layout="wide"
)


# ====================================================
# NAVIGATION
# ====================================================

pages = [

    st.Page(
        "pages/0_Homepage.py",
        title="Homepage",
        icon="🏠"
    ),

    st.Page(
        "pages/1_Statistics.py",
        title="EMS Statistics",
        icon="📊"
    ),

    st.Page(
        "pages/2_Data.py",
        title="Data",
        icon="📋"
    ),

    st.Page(
        "pages/3_Map.py",
        title="Map",
        icon="🗺️"
    )

]


# ====================================================
# RUN APP
# ====================================================

pg = st.navigation(pages)

pg.run()