# utils/ml_utils.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

def detect_anomalies(df: pd.DataFrame, features: list, contamination=0.05):
    """
    Detect anomalies in dataframe using Isolation Forest.

    Args:
        df (pd.DataFrame): Input data.
        features (list): List of feature column names to use.
        contamination (float): Expected proportion of anomalies.

    Returns:
        pd.Series: Anomaly labels (-1 for anomaly, 1 for normal).
    """
    clf = IsolationForest(contamination=contamination, random_state=42)
    clf.fit(df[features])
    preds = clf.predict(df[features])
    return pd.Series(preds, index=df.index)


def linear_regression_predict(df: pd.DataFrame, feature_cols: list, target_col: str):
    """
    Fit linear regression model and predict target.

    Args:
        df (pd.DataFrame): Input data.
        feature_cols (list): Feature columns.
        target_col (str): Target column.

    Returns:
        tuple: (model, predictions as np.array)
    """
    X = df[feature_cols].values
    y = df[target_col].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    return model, y_pred
