import pandas as pd

def clean_data(df):

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Convert dates
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Convert numeric columns
    df["Patient Age"] = pd.to_numeric(df["Patient Age"], errors="coerce")
    df["Call Duration"] = pd.to_numeric(df["Call Duration"], errors="coerce")
    df["How difficult was this call?"] = pd.to_numeric(
        df["How difficult was this call?"], errors="coerce"
    )

    return df