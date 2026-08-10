import streamlit as st
import plotly.express as px
import pandas as pd


def show_operations_analytics(df):

    st.header("🏥 Operations Analytics")

    # ====================================================
    # FIRST ROW
    # ====================================================

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Hospital Distribution
    # ----------------------------------------------------

    hospital_df = (
        df["Conveyed to which hospital"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    hospital_df.columns = [
        "Hospital",
        "Calls"
    ]

    hospital_fig = px.bar(
        hospital_df,
        x="Calls",
        y="Hospital",
        orientation="h",
        text="Calls",
        title="Hospital Distribution"
    )

    hospital_fig.update_layout(
        xaxis_title="Number of Patients",
        yaxis_title=""
    )

    left.plotly_chart(
        hospital_fig,
        use_container_width=True,
        key="hospital_chart"
    )



    # ----------------------------------------------------
    # Reason for Non-Conveyance
    # ----------------------------------------------------

    non_conveyance_df = (
        df["If not conveyed, what was the reason?"]
        .dropna()
    )

    # Remove entries that are not actual non-conveyance reasons
    non_conveyance_df = non_conveyance_df[
        ~non_conveyance_df.isin([
            "Not Applicable",
            "Conveyed",
            ""
        ])
    ]

    non_conveyance_df = (
        non_conveyance_df
        .value_counts()
        .reset_index()
    )

    non_conveyance_df.columns = [
        "Reason",
        "Count"
    ]

    non_conveyance_fig = px.pie(
        non_conveyance_df,
        values="Count",
        names="Reason",
        hole=0.5,
        title="Reason for Non-Conveyance"
    )

    right.plotly_chart(
        non_conveyance_fig,
        use_container_width=True,
        key="non_conveyance_chart"
    )




    # ====================================================
    # CALLS BY ALPHA / CALLSIGN
    # ====================================================

    st.subheader("Calls by Alpha / Callsign")

    callsign_df = (
        df["Alpha/ Callsign"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    callsign_df.columns = [
        "Alpha / Callsign",
        "Calls"
    ]

    # Sort so the highest value appears at the top
    callsign_df = callsign_df.sort_values(
        "Calls",
        ascending=True
    )

    callsign_fig = px.bar(
        callsign_df,
        x="Calls",
        y="Alpha / Callsign",
        orientation="h",
        text="Calls",
        title="Number of Calls by Alpha / Callsign"
    )

    callsign_fig.update_traces(
        textposition="outside"
    )

    callsign_fig.update_layout(
        xaxis_title="Number of Calls",
        yaxis_title=""
    )

    st.plotly_chart(
        callsign_fig,
        use_container_width=True,
        key="operations_callsign_chart"
    )


    # ====================================================
    # SECOND ROW
    # ====================================================

    col1, col2, col3, col4 = st.columns(4)

    callback_rate = (
        (df["Callback?"] == "Yes").mean() * 100
    )

    standby_rate = (
        (df["Standby?"] == "Yes").mean() * 100
    )

    police_rate = (
        (df["Police Dispatch?"] == "Yes").mean() * 100
    )

    divert_rate = (
        (df["Divert?"] == "Yes").mean() * 100
    )


    col1.metric(
        "Callback Rate",
        f"{callback_rate:.1f}%"
    )

    col2.metric(
        "Standby Rate",
        f"{standby_rate:.1f}%"
    )

    col3.metric(
        "Police Dispatch",
        f"{police_rate:.1f}%"
    )

    col4.metric(
        "Divert Rate",
        f"{divert_rate:.1f}%"
    )

