import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.figure_factory as ff


# ✅ Sayısal Kolonlar için Tanımlayıcı İstatistikler
def analyze_numeric(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame({"Message": ["No numeric columns found."]})
    
    desc = numeric_df.describe().T
    desc["missing"] = numeric_df.isnull().sum()
    desc["missing_percent"] = 100 * desc["missing"] / len(df)
    return desc


# ✅ Korelasyon Matrisi ve Plotly ile Görselleştirme
def correlation_plot(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None, pd.DataFrame()
    
    corr_matrix = numeric_df.corr().round(2)
    fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', origin='lower')
    fig.update_layout(title="Correlation Matrix", title_x=0.5)
    return fig, corr_matrix


# ✅ Ki-Kare Testi
def chi_square_analysis(df: pd.DataFrame, col1: str, col2: str):
    contingency_table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, _ = stats.chi2_contingency(contingency_table)

    result = {
        "chi2_stat": chi2,
        "p_value": p,
        "degrees_of_freedom": dof,
        "contingency_table": contingency_table
    }
    return result, p


# ✅ T-Test Analizi (Bağımsız Gruplar)
def t_test_analysis(df: pd.DataFrame, col1: str, col2: str):
    data1 = df[col1].dropna()
    data2 = df[col2].dropna()
    
    stat, p = stats.ttest_ind(data1, data2, equal_var=False)

    result = {
        "Column A": col1,
        "Column B": col2,
        "t_statistic": stat,
        "p_value": p,
        "mean_A": data1.mean(),
        "mean_B": data2.mean(),
        "std_A": data1.std(),
        "std_B": data2.std(),
        "n_A": len(data1),
        "n_B": len(data2)
    }

    return result, p
