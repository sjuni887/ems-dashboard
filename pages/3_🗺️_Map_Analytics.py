import streamlit as st
import pandas as pd
import plotly.express as px


from data.sheets import load_data
from data.cleaning import clean_data


# ====================================================
# PAGE SETUP
# ====================================================

st.set_page_config(
    page_title="Map Analytics",
    page_icon="🗺️",
    layout="wide"
)


# ====================================================
# LOAD DATA
# ====================================================

df = clean_data(load_data())

coordinates_df = pd.read_csv(
    "cache/location_coordinates.csv"
)


# ====================================================
# MERGE EMS DATA WITH COORDINATES
# ====================================================

map_df = df.merge(
    coordinates_df,
    left_on="Call location",
    right_on="Location",
    how="left"
)


# Keep only calls that have coordinates
mapped_df = map_df.dropna(
    subset=["Latitude", "Longitude"]
).copy()


# ====================================================
# PAGE TITLE
# ====================================================

st.title("🗺️ EMS Call Map")

st.caption(
    "Explore the geographical distribution of EMS calls."
)


# ====================================================
# FILTERS
# ====================================================

st.sidebar.header("Map Filters")


# ----------------------------------------------------
# PAC Filter
# ----------------------------------------------------

pac_options = sorted(
    mapped_df["Starting PAC status"]
    .dropna()
    .unique()
)

selected_pac = st.sidebar.multiselect(
    "Starting PAC",
    options=pac_options,
    default=pac_options
)


# ----------------------------------------------------
# Shift Filter
# ----------------------------------------------------

shift_options = sorted(
    mapped_df["Shift"]
    .dropna()
    .unique()
)

selected_shift = st.sidebar.multiselect(
    "Shift",
    options=shift_options,
    default=shift_options
)


# ----------------------------------------------------
# Call Type Filter
# ----------------------------------------------------

call_type_options = sorted(
    mapped_df["Call Type"]
    .dropna()
    .unique()
)

selected_call_type = st.sidebar.multiselect(
    "Call Type",
    options=call_type_options,
    default=call_type_options
)


# ====================================================
# APPLY FILTERS
# ====================================================

filtered_map_df = mapped_df[
    mapped_df["Starting PAC status"].isin(selected_pac)
    & mapped_df["Shift"].isin(selected_shift)
    & mapped_df["Call Type"].isin(selected_call_type)
].copy()


# ====================================================
# MAP SUMMARY
# ====================================================

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Calls Shown",
        len(filtered_map_df)
    )


with col2:
    st.metric(
        "Unique Locations",
        filtered_map_df["Call location"].nunique()
    )


with col3:
    st.metric(
        "Locations Without Coordinates",
        len(df) - len(mapped_df)
    )


st.divider()


# ====================================================
# MAP TABS
# ====================================================

normal_tab, heatmap_tab = st.tabs(
    [
        "📍 Normal Map",
        "🔥 Heatmap"
    ]
)


# ====================================================
# NORMAL MAP
# ====================================================

with normal_tab:

    st.subheader("📍 EMS Call Locations")

    normal_map_fig = px.scatter_map(
        filtered_map_df,
        lat="Latitude",
        lon="Longitude",

        hover_name="Call location",

        hover_data={
            "Latitude": False,
            "Longitude": False,
            "Starting PAC status": True,
            "Ending PAC Status": True,
            "Call Type": True,
            "Patient Age": True,
            "Call Duration": True
        },

        zoom=10,
        height=650
    )

    normal_map_fig.update_layout(
        map_style="open-street-map",

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(
        normal_map_fig,
        use_container_width=True,
        key="normal_ems_map"
    )


# ====================================================
# HEATMAP
# ====================================================

with heatmap_tab:

    st.subheader("🔥 EMS Call Density")

    heatmap_fig = px.density_map(
        filtered_map_df,
        lat="Latitude",
        lon="Longitude",

        radius=15,

        zoom=10,
        height=650
    )

    heatmap_fig.update_layout(
        map_style="open-street-map",

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(
        heatmap_fig,
        use_container_width=True,
        key="ems_heatmap"
    )
