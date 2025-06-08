import pandas as pd
import numpy as np
from rich import print

def generate_insights(df):
    insights = []

    # 1. Data Overview
    insights.append("--- Data Overview ---")
    total_rows = len(df)
    total_columns = df.shape[1]
    insights.append(f"Total rows: {total_rows}")
    insights.append(f"Total columns: {total_columns}")

    # 2. Missing Values
    insights.append("--- Missing Values ---")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if not missing_cols.empty:
        for col, miss_count in missing_cols.items():
            insights.append(f"Column '{col}' has {miss_count} missing values ({miss_count / total_rows:.2%})")
    else:
        insights.append("No missing values detected.")

    # 3. Duplicate Rows
    insights.append("--- Duplicate Rows ---")
    dup_count = df.duplicated().sum()
    insights.append(f"Duplicate rows: {dup_count}")

    # 4. Data Types
    insights.append("--- Data Types ---")
    type_counts = df.dtypes.value_counts()
    for dtype, count in type_counts.items():
        insights.append(f"{count} column(s) of type '{dtype}'")

    # 5. Unique Values and Cardinality
    insights.append("--- Unique Values & Cardinality ---")
    for col in df.columns:
        unique_vals = df[col].nunique(dropna=False)
        if unique_vals == 1:
            insights.append(f"Column '{col}' is constant (1 unique value)")
        elif unique_vals <= 10:
            examples = df[col].dropna().unique()
            insights.append(f"Column '{col}' has {unique_vals} unique values: {examples}")
        else:
            insights.append(f"Column '{col}' has {unique_vals} unique values")

    for col in df.select_dtypes(include='object'):
        if df[col].nunique() / total_rows > 0.5:
            insights.append(f"Column '{col}' has high cardinality ({df[col].nunique()} unique values)")

    # 6. Imbalanced Categorical Columns
    insights.append("--- Imbalanced Categorical Columns ---")
    for col in df.select_dtypes(include='object'):
        top_freq = df[col].value_counts(normalize=True, dropna=False).iloc[0]
        if top_freq > 0.9:
            top_val = df[col].value_counts().idxmax()
            insights.append(f"Column '{col}' is imbalanced — '{top_val}' occurs in {top_freq:.1%} of rows")
    if not any("is imbalanced" in i for i in insights[-3:]):
        insights.append("No highly imbalanced categorical columns found.")

    # 7. Numeric Column Statistics
    insights.append("--- Numeric Column Statistics ---")
    numeric_cols = df.select_dtypes(include='number')
    if not numeric_cols.empty:
        desc = numeric_cols.describe().T
        for col in desc.index:
            insights.append(
                f"Numeric column '{col}': mean={desc.loc[col, 'mean']:.2f}, std={desc.loc[col, 'std']:.2f}, "
                f"min={desc.loc[col, 'min']}, max={desc.loc[col, 'max']}"
            )

        # 8. Skewness
        insights.append("--- Skewness ---")
        skewness = numeric_cols.skew()
        for col, skew in skewness.items():
            if abs(skew) > 1:
                skew_label = "highly skewed"
            elif abs(skew) > 0.5:
                skew_label = "moderately skewed"
            else:
                skew_label = "approximately symmetric"
            insights.append(f"Column '{col}' is {skew_label} (skewness={skew:.2f})")

        # 9. Outliers (IQR Method)
        insights.append("--- Outliers (IQR Method) ---")
        for col in numeric_cols.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                insights.append(f"Column '{col}' has {outliers} potential outliers (IQR method)")
        if not any("potential outliers" in i for i in insights[-len(numeric_cols.columns):]):
            insights.append("No significant outliers detected in numeric columns.")

        # 10. Correlation
        insights.append("--- Correlation ---")
        corr = numeric_cols.corr()
        corr_pairs = corr.abs().unstack().sort_values(ascending=False)
        corr_pairs = corr_pairs[corr_pairs < 1]  # exclude self-correlation
        top_corr = corr_pairs.drop_duplicates().head(3)
        for (col1, col2), val in top_corr.items():
            insights.append(f"High correlation between '{col1}' and '{col2}': {val:.2f}")
        if top_corr.empty:
            insights.append("No strong correlations found between numeric columns.")

    # 11. Datetime Columns
    insights.append("--- Datetime Columns ---")
    datetime_cols = df.select_dtypes(include='datetime')
    if not datetime_cols.empty:
        for col in datetime_cols.columns:
            min_date = df[col].min()
            max_date = df[col].max()
            missing = df[col].isnull().sum()
            insights.append(f"Datetime column '{col}': range from {min_date} to {max_date}, missing: {missing}")
    else:
        insights.append("No datetime columns found.")

    # 12. Text Column Summary
    # Bold + Blue
    insights.append("--- Text Column Summary ---")
    # insights.append('<div style="font-weight:bold; color:blue; font-size:16px; margin-top:20px;">--- Text Column Summary ---</div>')

    object_cols = df.select_dtypes(include='object')
    for col in object_cols.columns:
        if df[col].apply(lambda x: isinstance(x, str)).mean() > 0.8:
            avg_len = df[col].dropna().apply(len).mean()
            insights.append(f"Text column '{col}' has average length {avg_len:.1f} characters")
      
 

    return insights
