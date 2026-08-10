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

pages = {
    "Home": [
        st.Page(
            "pages/0_Homepage.py",
            title="Homepage",
            icon="🏠"
        )
    ],

    "Analytics": [
        st.Page(
            "pages/1_Statistics.py",
            title="EMS Statistics",
            icon="📊"
        )
    ],

    "Data": [
        st.Page(
            "pages/2_Data.py",
            title="Data",
            icon="📋"
        )
    ],

    "Map": [
        st.Page(
            "pages/3_Map.py",
            title="Map",
            icon="🗺️"

        )
    ]

}


# ====================================================
# RUN APP
# ====================================================

pg = st.navigation(pages)

pg.run()
