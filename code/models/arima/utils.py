import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss

def check_stationarity(series, title="Time Series"):
    """Perform ADF and KPSS tests to check for stationarity."""
    print(f"--- Stationarity Tests for {title} ---")
    
    # ADF Test
    adf_result = adfuller(series.dropna())
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"ADF p-value: {adf_result[1]:.4f}")
    print("ADF Critical Values:")
    for key, value in adf_result[4].items():
        print(f"   {key}: {value:.4f}")
        
    # KPSS Test
    kpss_result = kpss(series.dropna(), nlags='auto')
    print(f"KPSS Statistic: {kpss_result[0]:.4f}")
    print(f"KPSS p-value: {kpss_result[1]:.4f}")
    print("KPSS Critical Values:")
    for key, value in kpss_result[3].items():
        print(f"   {key}: {value:.4f}")
    
    if adf_result[1] < 0.05 and kpss_result[1] > 0.05:
        print("Conclusion: The series is likely stationary.")
    else:
        print("Conclusion: The series is likely non-stationary.")

def plot_decomposition(series, model='additive', period=7):
    """Plot seasonal decomposition of the time series."""
    from statsmodels.tsa.seasonal import seasonal_decompose
    result = seasonal_decompose(series.dropna(), model=model, period=period)
    fig = result.plot()
    fig.set_size_inches(12, 10)
    plt.tight_layout()
    plt.show()
