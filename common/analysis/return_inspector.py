import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import vectorbt as vbt
from common.util.stats import get_return_metrics

def inspect_returns(
    strat_returns: pd.Series,
    benchmark_returns: pd.Series = None,
    strat_name="Strategy",
    bench_name="Benchmark"
):
    strat_returns = strat_returns.dropna()
    metrics = get_return_metrics(strat_returns, strat_name)
    print(f"\n📈 Performance for {strat_name}")
    for k, v in metrics.items():
        if k != "name":
            print(f"  {k.replace('_',' ').title():15}: {v:.2%}" if v is not None else "")

    if benchmark_returns is not None:
        benchmark_returns = benchmark_returns.dropna()
        df = pd.concat([strat_returns, benchmark_returns], axis=1).dropna()
        df.columns = [strat_name, bench_name]
        df.cumsum().apply(lambda x: (1 + x).cumprod()).plot(figsize=(12, 4),
                                                              title=f"{strat_name} vs {bench_name}")

    else:
        (1 + strat_returns).cumprod().plot(figsize=(12,4), title=strat_name)

    plt.grid(True)
    plt.show()

    sns.histplot(strat_returns, bins=50, kde=True)
    plt.title(f"{strat_name} Distribution")
    plt.show()

    monthly = strat_returns.resample("M").apply(lambda x: (1 + x).prod() - 1)
    tbl = monthly.reset_index()
    tbl['Year'] = tbl['date'].dt.year
    tbl['Month'] = tbl['date'].dt.strftime('%b')
    heat = tbl.pivot("Year", "Month", "return")
    sns.heatmap(heat, annot=True, fmt=".1%", cmap="RdYlGn", center=0)
    plt.title(f"{strat_name} Monthly Returns")
    plt.show()
