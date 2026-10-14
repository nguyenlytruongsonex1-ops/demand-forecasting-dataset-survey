"""Hàm dùng chung cho các notebook EDA."""
import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL

def overview(df):
    """Bảng kiểu dữ liệu, số thiếu, số giá trị khác nhau."""
    return pd.DataFrame({"dtype": df.dtypes.astype(str), "n_missing": df.isna().sum(),
                         "pct_missing": (df.isna().mean()*100).round(3), "n_unique": df.nunique()})

def time_gaps(t, freq):
    """Số mốc thời gian bị thiếu so với lưới đều, và số mốc trùng."""
    t = pd.Series(pd.to_datetime(t))
    full = pd.date_range(t.min(), t.max(), freq=freq)
    missing = full.difference(pd.DatetimeIndex(t.unique()))
    return {"start": t.min(), "end": t.max(), "n_expected": len(full), "n_unique": t.nunique(),
            "n_missing_steps": len(missing), "n_duplicated_ts": int(t.duplicated().sum())}, missing

def shape_stats(df):
    """Thống kê mô tả + skewness, kurtosis (excess) cho cột số."""
    num = df.select_dtypes("number")
    d = num.describe().T
    d["skew"] = num.skew(); d["kurtosis"] = num.kurt()
    return d.round(3)

def iqr_outliers(df, k=1.5):
    """Số và tỉ lệ outlier theo quy tắc IQR (k*IQR)."""
    rows = {}
    for c in df.select_dtypes("number"):
        s = df[c].dropna(); q1, q3 = s.quantile([.25, .75]); i = q3 - q1
        n = int(((s < q1-k*i) | (s > q3+k*i)).sum())
        rows[c] = {"lower": q1-k*i, "upper": q3+k*i, "n_outliers": n, "pct": round(100*n/len(s), 3)}
    return pd.DataFrame(rows).T

def plot_dists(df, cols, bins=50):
    n = len(cols); fig, ax = plt.subplots(1, n, figsize=(3.2*n, 2.8))
    ax = np.atleast_1d(ax)
    for a, c in zip(ax, cols):
        a.hist(df[c].dropna(), bins=bins, color="steelblue"); a.set_title(f"{c}\nskew={df[c].skew():.2f}", fontsize=9)
    plt.tight_layout(); plt.show()

def stationarity(s, name="", regression="c"):
    """ADF (H0: có nghiệm đơn vị, không dừng) và KPSS (H0: dừng)."""
    s = pd.Series(s).dropna().astype(float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        adf = adfuller(s, autolag="AIC")
        kp = kpss(s, regression=regression, nlags="auto")
    adf_ok, kp_ok = adf[1] < 0.05, kp[1] >= 0.05
    verdict = ("dừng" if adf_ok and kp_ok else "không dừng" if not adf_ok and not kp_ok
               else "trái chiều: ADF nói dừng, KPSS nói không dừng (thường do xu hướng/mùa vụ → kiểm lại sau sai phân)" if adf_ok
               else "trái chiều: ADF nói không dừng, KPSS nói dừng (có thể dừng quanh xu hướng)")
    return {"series": name, "n": len(s), "ADF_stat": round(adf[0], 3), "ADF_p": round(adf[1], 4),
            "KPSS_stat": round(kp[0], 3), "KPSS_p(bị chặn 0.01-0.1)": round(kp[1], 4), "kết luận": verdict}

def acf_pacf(s, lags, title=""):
    s = pd.Series(s).dropna().astype(float)
    fig, ax = plt.subplots(1, 2, figsize=(12, 3))
    plot_acf(s, lags=lags, ax=ax[0]); plot_pacf(s, lags=min(lags, len(s)//2-1), ax=ax[1], method="ywm")
    ax[0].set_title(f"ACF {title}"); ax[1].set_title(f"PACF {title}"); plt.tight_layout(); plt.show()

def autocorrs(s, lags):
    s = pd.Series(s).astype(float); return {f"lag{l}": round(s.autocorr(l), 3) for l in lags}

def stl_strength(s, period, robust=False, plot=True, title=""):
    """STL + độ mạnh xu hướng/mùa vụ (Wang, Smith & Hyndman 2006)."""
    s = pd.Series(s).astype(float)
    r = STL(s, period=period, robust=robust).fit()
    ft = max(0, 1 - r.resid.var()/(r.trend+r.resid).var()); fs = max(0, 1 - r.resid.var()/(r.seasonal+r.resid).var())
    if plot:
        fig = r.plot(); fig.set_size_inches(12, 6); fig.suptitle(title, y=1.01); plt.show()
    return {"trend_strength": round(ft, 3), "seasonal_strength": round(fs, 3)}
