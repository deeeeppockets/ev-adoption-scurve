"""Model definitions and fitting helpers shared by all analysis scripts.

Logistic model (solution of the logistic ODE dP/dt = r P (1 - P/K)):
    P(t) = K / (1 + exp(-r (t - t0)))
Exponential model (solution of dP/dt = b P, i.e. the logistic with K -> infinity):
    P(t) = a exp(b (t - 2010))
Naive benchmark: straight-line extrapolation of the last 3 observed years.
"""
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import OptimizeWarning, curve_fit

DATA = "data/raw/electric-car-sales-share.csv"
T_REF = 2010  # reference year for the exponential model


def logistic(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))


def exponential(t, a, b):
    return a * np.exp(b * (t - T_REF))


def load_countries(path=DATA, min_years=10):
    """Country-level rows only (drops OWID aggregates such as World, EU, Europe).

    Keeps countries with at least `min_years` observations that run to 2025.
    """
    d = pd.read_csv(path)
    d = d[d.code.notna() & ~d.code.astype(str).str.startswith("OWID")]
    n = d.groupby("entity").year.agg(["count", "max"])
    keep = n[(n["count"] >= min_years) & (n["max"] == d.year.max())].index
    return d[d.entity.isin(keep)].sort_values(["entity", "year"]).reset_index(drop=True)


def series(d, country, end=None):
    s = d[d.entity == country]
    if end is not None:
        s = s[s.year <= end]
    return s.year.to_numpy(float), s.ev_sales_share.to_numpy(float)


def fit_logistic(t, y):
    """Least-squares fit of the logistic curve.

    Bounds: the ceiling K lies between the highest share observed so far and 100 %;
    r in [0.01, 3] per year; t0 in [2000, 2060].
    Returns (K, r, t0).
    """
    ymax = max(y.max(), 0.1)
    p0 = [min(100.0, max(2 * ymax, 10.0)), 0.5, t[-1]]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OptimizeWarning)
        p, _ = curve_fit(logistic, t, y, p0=p0,
                         bounds=([ymax, 0.01, 2000], [100, 3, 2060]), maxfev=50000)
    return p


def fit_exponential(t, y):
    """Least-squares fit of the exponential curve. Returns (a, b)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OptimizeWarning)
        p, _ = curve_fit(exponential, t, y, p0=[0.1, 0.3],
                         bounds=([1e-6, 0], [100, 3]), maxfev=50000)
    return p


def naive_forecast(t, y, t_new):
    """Extend the straight line through the last 3 observations; clip to [0, 100] %."""
    slope, intercept = np.polyfit(t[-3:], y[-3:], 1)
    return np.clip(slope * np.asarray(t_new, float) + intercept, 0, 100)


def aic(y, y_hat, k):
    """Akaike Information Criterion for least squares with Gaussian errors.

    AIC = n ln(RSS / n) + 2k, where k is the number of fitted parameters.
    Lower is better; a difference above ~2 is meaningful.
    """
    n = len(y)
    rss = max(np.sum((y - y_hat) ** 2), 1e-12)
    return n * np.log(rss / n) + 2 * k
