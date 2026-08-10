import streamlit as st
import plotly.express as px
import pandas as pd


def show_call_analytics(df):

    st.header("📞 Call Analytics")

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Calls by Day of Week
    # ----------------------------------------------------

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday_df = (
        df["Day of Week"]
        .value_counts()
        .reindex(weekday_order, fill_value=0)
        .reset_index()
    )

    weekday_df.columns = ["Day", "Calls"]

    weekday_fig = px.bar(
        weekday_df,
        x="Calls",
        y="Day",
        orientation="h",
        text="Calls",
        title="Calls by Day of Week"
    )

    weekday_fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=weekday_order[::-1]
        ),
        xaxis_title="Number of Calls",
        yaxis_title=""
    )

    left.plotly_chart(
        weekday_fig,
        use_container_width=True,
        key="weekday_chart"
    )

    # ----------------------------------------------------
    # Calls by Shift
    # ----------------------------------------------------

    shift_df = (
        df["Shift"]
        .value_counts()
        .reset_index()
    )

    shift_df.columns = ["Shift", "Calls"]

    shift_fig = px.bar(
        shift_df,
        x="Shift",
        y="Calls",
        text="Calls",
        title="Calls by Shift"
    )

    shift_fig.update_layout(
        xaxis_title="Shift",
        yaxis_title="Number of Calls"
    )

    right.plotly_chart(
        shift_fig,
        use_container_width=True,
        key="shift_chart"
    )

    # ====================================================

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Difficulty
    # ----------------------------------------------------

    difficulty_df = (
        df["How difficult was this call?"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    difficulty_df.columns = ["Difficulty", "Calls"]

    difficulty_fig = px.bar(
        difficulty_df,
        x="Difficulty",
        y="Calls",
        text="Calls",
        title="Call Difficulty Distribution"
    )

    difficulty_fig.update_layout(
        xaxis_title="Difficulty",
        yaxis_title="Number of Calls"
    )

    left.plotly_chart(
        difficulty_fig,
        use_container_width=True,
        key="difficulty_chart"
    )

    # ----------------------------------------------------
    # Average Duration by Day
    # ----------------------------------------------------

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    duration_df = (
        df.groupby("Day of Week")["Call Duration"]
        .mean()
        .reindex(weekday_order)
        .reset_index()
    )

    duration_df.columns = ["Day", "Average Duration"]

    duration_fig = px.bar(
        duration_df,
        x="Average Duration",
        y="Day",
        orientation="h",
        text=duration_df["Average Duration"].round(1),
        title="Average Call Duration by Day"
    )

    duration_fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=weekday_order[::-1]
        ),
        xaxis_title="Average Duration (mins)",
        yaxis_title=""
    )

    right.plotly_chart(
        duration_fig,
        use_container_width=True,
        key="duration_by_day_chart"
    )

    call_type_counts = (
    df["Call Type"]
    .value_counts()
    .reset_index()
)

    call_type_counts.columns = [
    "Call Type",
    "Calls"
    ]

    fig = px.pie(
        call_type_counts,
        names="Call Type",
        values="Calls",
        hole=0.4
    )

    fig.update_layout(
        title="Calls by Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="call_type_pie"
    )