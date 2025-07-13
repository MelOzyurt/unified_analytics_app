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

        # Histogram for selected column
        col = st.selectbox("Select column to plot histogram", numeric_cols)
        st.bar_chart(df[col])

    elif option == "Anomaly Detection":
        st.subheader("Anomaly Detection with Isolation Forest")

        contamination = st.slider("Contamination (expected outliers %)", 0.01, 0.2, 0.05)

        clf = IsolationForest(contamination=contamination, random_state=42)
        preds = clf.fit_predict(df[numeric_cols])
        df["anomaly"] = preds
        st.write("Anomalies detected (-1 indicates anomaly):")
        st.dataframe(df[df["anomaly"] == -1])

    elif option == "Trends and Anomalies":
        st.subheader("Trends and Anomalies")

        time_col = st.selectbox("Select time column (optional, if exists)", df.columns)
        target_col = st.selectbox("Select target numeric column", numeric_cols)

        if time_col:
            try:
                df[time_col] = pd.to_datetime(df[time_col])
                df_sorted = df.sort_values(time_col)
                df_sorted.set_index(time_col, inplace=True)

                # Rolling mean
                window = st.slider("Rolling window size", 3, 30, 7)
                rolling_mean = df_sorted[target_col].rolling(window=window).mean()

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df_sorted[target_col], label="Original")
                ax.plot(rolling_mean, label=f"Rolling Mean (window={window})")

                # Simple anomaly detection where actual deviates from rolling mean by 2 std
                residual = df_sorted[target_col] - rolling_mean
                std_dev = residual.std()
                anomalies = residual.abs() > (2 * std_dev)

                ax.scatter(df_sorted.index[anomalies], df_sorted[target_col][anomalies], color='r', label="Anomalies")
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error processing time column: {e}")
        else:
            st.info("Please select a valid time column.")

    elif option == "Prediction Analysis":
        st.subheader("Prediction Analysis (Linear Regression)")

        feature_cols = st.multiselect("Select feature columns (numeric)", numeric_cols, default=numeric_cols[:-1])
        target_col = st.selectbox("Select target column (numeric)", numeric_cols)

        if feature_cols and target_col:
            X = df[feature_cols].values
            y = df[target_col].values

            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)

            st.write("Regression Coefficients:")
            coef_df = pd.DataFrame({
                "Feature": feature_cols,
                "Coefficient": model.coef_
            })
            st.dataframe(coef_df)

            # Plot actual vs predicted
            fig, ax = plt.subplots()
            ax.scatter(y, y_pred)
            ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
            ax.set_xlabel("Actual")
            ax.set_ylabel("Predicted")
            ax.set_title("Actual vs Predicted")
            st.pyplot(fig)
        else:
            st.info("Select at least one feature and one target column.")

