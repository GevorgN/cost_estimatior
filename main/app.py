import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import clean

st.set_page_config(page_title="Daily Income & Expense Tracker", layout="centered")

st.title("📊 Daily Income & Expense Tracker")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")

    # Drop fully empty columns
    new_columns = [
    'Date',
    'Online Date',
    'Amount',
    'Currency',
    'Credit',
    'Debit',
    'Applicable exchange rate',
    'Final Account Balance',
    'Transaction description'
    ]
    # Step 2: Find the header row index where 'Date' appears
    header_row_idx = None
    for idx, row in df.iterrows():
        if row.astype(str).str.contains('Date', case=False).any():
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise ValueError("Header row with 'Date' not found.")

    daily_summary = clean(df, new_columns)

    st.subheader("📅 Daily Summary")
    st.dataframe(daily_summary)

    # Chart type selection
    chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Pie"])

    if chart_type == "Line":
        st.line_chart(daily_summary.set_index("Day"))

    elif chart_type == "Bar":
        st.bar_chart(daily_summary.set_index("Day"))

    elif chart_type == "Pie":
        total_credit = daily_summary["Credit"].sum()
        total_debit = daily_summary["Debit"].sum()

        fig, ax = plt.subplots()
        ax.pie(
            [total_credit, total_debit],
            labels=["Credit", "Debit"],
            autopct="%1.1f%%",
            colors=["#A7182B", "#1E21CF"]
        )
        ax.set_title("Total Credit vs Debit")
        st.pyplot(fig)
