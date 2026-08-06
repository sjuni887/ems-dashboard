import streamlit as st
import plotly.express as px
import pandas as pd


def show_pac_analytics(df):

    st.header("🚨 PAC Analytics")

    # ----------------------------------------------------
    # PAC Information
    # ----------------------------------------------------

    with st.expander("ℹ️ How to read PAC Status"):

        st.markdown("""
### What is PAC?

PAC (Patient Acuity Category) represents the patient's clinical priority.

| PAC | Description |
|------|-------------|
| **P1+** | Highest priority / immediately life-threatening |
| **P1** | Critical patient requiring urgent intervention |
| **P2** | Serious but stable |
| **P3** | Stable / non-urgent patient |

### Understanding these charts

- **Starting PAC** – Priority assigned when the case was dispatched.
- **Ending PAC** – Final PAC after patient assessment.
- **P1+ Downgraded** – Percentage of **P1+** dispatches that became **P2 or P3**.
- **PAC Unchanged** – Cases where the starting and ending PAC remained the same.
- **Case Upgrade Rate** – Percentage of calls upgraded during the incident.
- **PAC Conversion Matrix** – Shows how dispatch PAC changed after patient assessment.
""")

    pac_order = ["P1+", "P1", "P2", "P3"]

    left, right = st.columns(2)

    # ----------------------------------------------------
    # Starting PAC
    # ----------------------------------------------------

    starting_pac_df = (
        df["Starting PAC status"]
        .value_counts()
        .reindex(pac_order, fill_value=0)
        .reset_index()
    )

    starting_pac_df.columns = ["PAC", "Calls"]

    starting_pac_fig = px.bar(
        starting_pac_df,
        x="Calls",
        y="PAC",
        orientation="h",
        text="Calls",
        title="Starting PAC Status"
    )

    starting_pac_fig.update_layout(
        xaxis_title="Number of Calls",
        yaxis_title=""
    )

    left.plotly_chart(
        starting_pac_fig,
        use_container_width=True,
        key="starting_pac_chart"
    )

    # ----------------------------------------------------
    # Ending PAC
    # ----------------------------------------------------

    ending_pac_df = (
        df["Ending PAC Status"]
        .value_counts()
        .reindex(pac_order, fill_value=0)
        .reset_index()
    )

    ending_pac_df.columns = ["PAC", "Calls"]

    ending_pac_fig = px.bar(
        ending_pac_df,
        x="Calls",
        y="PAC",
        orientation="h",
        text="Calls",
        title="Ending PAC Status"
    )

    ending_pac_fig.update_layout(
        xaxis_title="Number of Calls",
        yaxis_title=""
    )

    right.plotly_chart(
        ending_pac_fig,
        use_container_width=True,
        key="ending_pac_chart"
    )

    # ====================================================

    st.subheader("🔄 PAC Conversion Matrix")

    conversion_df = pd.crosstab(
        df["Starting PAC status"],
        df["Ending PAC Status"]
    )

    conversion_df = conversion_df.reindex(
        index=pac_order,
        columns=pac_order,
        fill_value=0
    )

    pac_conversion_fig = px.imshow(
        conversion_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Starting PAC → Ending PAC"
    )

    pac_conversion_fig.update_layout(
        xaxis_title="Ending PAC Status",
        yaxis_title="Starting PAC Status"
    )

    st.plotly_chart(
        pac_conversion_fig,
        use_container_width=True,
        key="pac_conversion_chart"
    )

    # ====================================================

    st.subheader("📌 PAC Summary")

    p1_calls = df[df["Starting PAC status"] == "P1+"]

    lower_pac = ["P2", "P3"]

    p1_downgraded = p1_calls[
        p1_calls["Ending PAC Status"].isin(lower_pac)
    ]

    p1_downgrade_rate = (
        len(p1_downgraded) / len(p1_calls) * 100
        if len(p1_calls) > 0
        else 0
    )

    unchanged = (
        df["Starting PAC status"] ==
        df["Ending PAC Status"]
    ).sum()

    unchanged_rate = (
        unchanged / len(df) * 100
        if len(df) > 0
        else 0
    )

    upgrade_rate = (
        (df["Case upgraded?"] == "Yes").mean() * 100
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "P1+ Downgraded",
            f"{len(p1_downgraded)} ({p1_downgrade_rate:.1f}%)"
        )

    with col2:
        st.metric(
            "PAC Unchanged",
            f"{unchanged} ({unchanged_rate:.1f}%)"
        )

    with col3:
        st.metric(
            "Case Upgrade Rate",
            f"{upgrade_rate:.1f}%"
        )