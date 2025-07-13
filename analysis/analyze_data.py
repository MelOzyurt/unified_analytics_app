# analysis/analyze_data.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_data_ui(df: pd.DataFrame):
    st.header("🔍 Analyze Data")

    if df is None or df.empty:
        st.warning("No data provided or empty dataframe.")
        return

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("No numeric columns found for analysis.")
        return

    st.write("### Select sub-analysis type:")
    option = st.selectbox("", [
        "Descriptive Analysis",
        "Anomaly Detection",
        "Trends and Anomalies",
        "Prediction Analysis"
    ])

    if option == "Descriptive Analysis":
        st.subheader("Descriptive Statistics")
        st.write(df[numeric_cols].describe())

        col = st.selectbox("Select column to plot histogram", numeric_cols)
        st.bar_chart(df[col])

    elif option == "Anomaly Detection":
        st.subheader("Anomaly Detection with Isolation Forest")

        contamination = st.slider("Contamination (expected outliers %)", 0.01, 0.2, 0.05)

        clf = IsolationForest(contamination=contamination, random_state=42)
        preds = clf.fit_predict(df[numeric_cols])

        df_copy = df.copy()
        df_copy["anomaly"] = preds
        st.write("Anomalies detected (-1 indicates anomaly):")
        st.dataframe(df_copy[df_copy["anomaly"] == -1])

    elif option == "Trends and Anomalies":
        st.subheader("Trends and Anomalies")

        # Filter columns that could be datetime
        possible_time_cols = df.columns[df.dtypes.isin([np.dtype('O'), 'datetime64[ns]'])].tolist()
        time_col = st.selectbox("Select time column (optional)", [""] + possible_time_cols)

        if time_col:
            try:
                df_copy = df.copy()
                df_copy[time_col] = pd.to_datetime(df_copy[time_col], errors='coerce')

                # Drop rows where time_col couldn't be converted
                df_clean = df_copy.dropna(subset=[time_col])
                if df_clean.empty:
                    st.error("No valid dates found in the selected time column.")
                    return

                df_sorted = df_clean.sort_values(time_col)
                df_sorted.set_index(time_col, inplace=True)

                target_col = st.selectbox("Select target numeric column", numeric_cols)

                window = st.slider("Rolling window size", 3, 30, 7)
                rolling_mean = df_sorted[target_col].rolling(window=window).mean()

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df_sorted[target_col], label="Original")
                ax.plot(rolling_mean, label=f"Rolling Mean (window={window})")

                residual = df_sorted[target_col] - rolling_mean
                std_dev = residual.std()
                anomalies = residual.abs() > (2 * std_dev)

                ax.scatter(df_sorted.index[anomalies], df_sorted[target_col][anomalies], color='r', label="Anomalies")
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error processing time column: {e}")
        else:
            st.info("Please select a valid time column to analyze trends.")

    elif option == "Prediction Analysis":
        st.subheader("Prediction Analysis (Linear Regression)")

        default_features = numeric_cols[:-1] if len(numeric_cols) > 1 else numeric_cols
        feature_cols = st.multiselect("Select feature columns (numeric)", numeric_cols, default=default_features)
        target_col = st.selectbox("Select target column (numeric)", numeric_cols)

        if feature_cols and target_col:
            if target_col in feature_cols:
                st.warning("Target column should not be in features.")
                return

            X = df[feature_cols].values
            y = df[target_col].values

            try:
                model = LinearRegression()
                model.fit(X, y)
                y_pred = model.predict(X)

                st.write("Regression Coefficients:")
                coef_df = pd.DataFrame({
                    "Feature": feature_cols,
                    "Coefficient": model.coef_
                })
                st.dataframe(coef_df)

                fig, ax = plt.subplots()
                ax.scatter(y, y_pred, alpha=0.7)
                ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
                ax.set_xlabel("Actual")
                ax.set_ylabel("Predicted")
                ax.set_title("Actual vs Predicted")
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Failed to fit model: {e}")

        else:
            st.info("Select at least one feature and one target column.")
