import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from common.utils.stats import get_return_metrics

__all__ = [
    "inspect_returns",
    "summary_table",
    "plot_equity",
    "plot_drawdown",
    "plot_rolling_sharpe",
    "plot_monthly_heatmap",
]

# ---------- core inspector ----------

def inspect_returns(
    strat_returns: pd.Series,
    benchmark_returns: pd.Series | None = None,
    strat_name: str = "Strategy",
    bench_name: str = "Benchmark",
):
    """Print metrics and show equity, drawdown, rolling Sharpe, and monthly heatmap."""
    r = _to_returns_series(strat_returns, name=strat_name)

    # 1) Metrics
    m = get_return_metrics(r)
    _print_metrics(m, strat_name)

    # 2) Optional benchmark (aligned to common index)
    bench = None
    if benchmark_returns is not None:
        bench = _to_returns_series(benchmark_returns, name=bench_name)
        common_idx = r.index.intersection(bench.index)
        r = r.loc[common_idx]
        bench = bench.loc[common_idx]

    # 3) Plots
    plot_equity(r, bench=bench, title=f"{strat_name} vs {bench_name}" if bench is not None else strat_name)
    plot_drawdown(r, title=f"{strat_name} Drawdown")
    plot_rolling_sharpe(r, window=126)
    plot_monthly_heatmap(r, title=f"{strat_name} Monthly Return Heatmap")

    return m  # handy to capture programmatically


# ---------- helpers & individual plots ----------

def summary_table(rets: pd.Series) -> pd.DataFrame:
    r = _to_returns_series(rets)
    m = get_return_metrics(r)
    return pd.DataFrame([{
        "N": m["n"],
        "Mean (daily)": m["mean"],
        "Std (daily)": m["std"],
        "Sharpe (ann)": m["sharpe"],
        "CAGR": m["cagr"],
        "MaxDD": m["max_dd"],
        "Win rate": m["win_rate"],
    }])


def plot_equity(rets: pd.Series, bench: pd.Series | None = None, title: str = "Equity Curve"):
    r = _to_returns_series(rets)
    eq = (1.0 + r).cumprod()
    ax = eq.plot(figsize=(11, 4), label=rets.name or "Strategy")
    if bench is not None:
        b = _to_returns_series(bench).reindex(eq.index).fillna(0.0)
        (1.0 + b).cumprod().plot(ax=ax, label=bench.name or "Benchmark", alpha=0.8)
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
    plt.show()

    # Distribution
    try:
        sns.histplot(r, bins=50, kde=True)
    except Exception:
        plt.hist(r.values, bins=50, alpha=0.9)
    plt.title(f"{rets.name or 'Strategy'} Return Distribution")
    plt.grid(True, axis="y", alpha=0.25)
    plt.show()


def plot_drawdown(rets: pd.Series, title: str = "Drawdown"):
    r = _to_returns_series(rets)
    eq = (1.0 + r).cumprod()
    dd = eq / eq.cummax() - 1.0
    ax = dd.plot(figsize=(11, 3), color="tab:red")
    ax.set_title(title)
    ax.grid(True)
    plt.show()


def plot_rolling_sharpe(rets: pd.Series, window: int = 126, title: str | None = None):
    r = _to_returns_series(rets)
    roll_mu = r.rolling(window).mean()
    roll_sd = r.rolling(window).std().replace(0, np.nan)
    roll_sh = np.sqrt(252) * (roll_mu / roll_sd)
    ax = roll_sh.plot(figsize=(11, 3))
    ax.set_title(title or f"Rolling Sharpe ({window}d)")
    ax.grid(True)
    plt.show()


def plot_monthly_heatmap(rets: pd.Series, title: str = "Monthly Return Heatmap"):
    r = _to_returns_series(rets)
    if r.empty:
        return
    monthly = r.resample("M").apply(lambda x: (1 + x).prod() - 1)
    monthly.name = "ret"
    df = monthly.to_frame()
    df["Year"] = df.index.year
    df["MonthNum"] = df.index.month
    df["Month"] = pd.Categorical(
        df.index.strftime("%b"),
        categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        ordered=True,
    )
    piv = df.pivot_table(index="Year", columns="Month", values="ret", aggfunc="first")
    fig, ax = plt.subplots(figsize=(11, 4))
    try:
        sns.heatmap(piv, annot=True, fmt=".1%", cmap="RdYlGn", center=0, cbar=True)
    except Exception:
        # Fallback plain imshow
        im = ax.imshow(piv.values, aspect="auto", cmap="RdYlGn", vmin=-0.2, vmax=0.2)
        ax.set_yticks(range(len(piv.index))); ax.set_yticklabels(piv.index)
        ax.set_xticks(range(12)); ax.set_xticklabels(piv.columns)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


# ---------- internal utilities ----------

def _to_returns_series(x: pd.Series | pd.DataFrame | np.ndarray, name: str | None = None) -> pd.Series:
    """Ensure a clean float Series with a DatetimeIndex."""
    s = pd.Series(x).copy()
    if not isinstance(s.index, pd.DatetimeIndex):
        # Try to coerce if it's e.g. a RangeIndex but you passed a DataFrame with a Date column
        s.index = pd.to_datetime(s.index, errors="ignore")
    s = s.dropna().astype(float).sort_index()
    if name is not None:
        s.name = name
    return s


def _print_metrics(m: dict, strat_name: str):
    print(f"\n📈 Performance for {strat_name}")
    # Format intelligently by key
    fmt = {
        "n": lambda v: f"{int(v)}",
        "mean": lambda v: f"{v:.3%}",
        "std": lambda v: f"{v:.3%}",
        "sharpe": lambda v: f"{v:.2f}",
        "cagr": lambda v: f"{v:.2%}",
        "max_dd": lambda v: f"{v:.2%}",
        "win_rate": lambda v: f"{v:.2%}",
    }
    order = ["n", "mean", "std", "sharpe", "cagr", "max_dd", "win_rate"]
    for k in order:
        v = m.get(k, None)
        if v is None:
            continue
        f = fmt.get(k, lambda x: str(x))
        label = k.replace("_", " ").title()
        print(f"  {label:12}: {f(v)}")
