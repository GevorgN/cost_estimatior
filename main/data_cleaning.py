import pandas as pd

def clean(df, new_columns):
    df = df.dropna(axis=1, how='all')  # Drop fully empty columns

    non_null_counts = df.notnull().sum()
    mean_non_nulls = non_null_counts.mean() / 2  # Half the average non-nulls
    df = df.loc[:, non_null_counts >= mean_non_nulls]

    df.columns = new_columns[:len(df.columns)]  # Rename columns safely

    df = df.dropna(subset=['Date'])  # Drop rows with no Date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows where Date failed conversion

    df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
    df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce').fillna(0)

    # Group by Date
    daily_summary = df.groupby(df['Date'].dt.date).agg({
        'Credit': 'sum',
        'Debit': 'sum'
    }).reset_index().rename(columns={'Date': 'Day'})

    return daily_summary
