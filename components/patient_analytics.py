import streamlit as st
import plotly.express as px
import pandas as pd


def show_patient_analytics(df):

    st.header("👤 Patient Analytics")

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Age Distribution
    # ----------------------------------------------------

    age_distribution_fig = px.histogram(
        df,
        x="Patient Age",
        nbins=20,
        title="Patient Age Distribution"
    )

    age_distribution_fig.update_layout(
        xaxis_title="Patient Age",
        yaxis_title="Number of Patients"
    )

    left.plotly_chart(
        age_distribution_fig,
        use_container_width=True,
        key="age_distribution_chart"
    )

    # ----------------------------------------------------
    # Gender Distribution
    # ----------------------------------------------------

    gender_df = (
        df["Patient Gender"]
        .value_counts()
        .reset_index()
    )

    gender_df.columns = ["Gender", "Count"]

    gender_distribution_fig = px.pie(
        gender_df,
        values="Count",
        names="Gender",
        hole=0.55,
        title="Patient Gender"
    )

    right.plotly_chart(
        gender_distribution_fig,
        use_container_width=True,
        key="gender_distribution_chart"
    )