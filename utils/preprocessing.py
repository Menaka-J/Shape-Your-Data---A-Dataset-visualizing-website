import pandas as pd

def preprocess_dataset(df):
    # Example preprocessing steps
    # 1. Drop duplicates
    df = df.drop_duplicates()
    # 2. Fill missing numeric values with mean
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col].fillna(df[col].mean(), inplace=True)
    # 3. Fill missing categorical with mode
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    return df
