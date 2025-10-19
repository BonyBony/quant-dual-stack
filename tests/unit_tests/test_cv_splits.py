import numpy as np
import pandas as pd

from research.modeling.cv import PurgedKFoldEmbargo


def make_panel(days: int = 50, symbols: int = 3) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=days, freq="D")
    idx = pd.MultiIndex.from_product([dates, [f"SYM{i}" for i in range(symbols)]], names=["date", "symbol"])
    values = np.arange(len(idx))
    return pd.DataFrame({"value": values}, index=idx)


def test_purged_kfold_no_overlap():
    panel = make_panel()
    cv = PurgedKFoldEmbargo(n_splits=5, embargo=2)
    for train_idx, test_idx in cv.split(panel):
        train_dates = panel.index.get_level_values("date")[train_idx]
        test_dates = panel.index.get_level_values("date")[test_idx]

        assert len(set(train_idx).intersection(test_idx)) == 0

        min_test = test_dates.min()
        max_test = test_dates.max()
        embargo_start = min_test - pd.Timedelta(days=cv.embargo)
        embargo_end = max_test + pd.Timedelta(days=cv.embargo)
        assert not any((train_dates >= embargo_start) & (train_dates <= embargo_end))


def test_purged_kfold_with_dates_argument():
    panel = make_panel()
    dates = panel.index.get_level_values("date")
    cv = PurgedKFoldEmbargo(n_splits=3, embargo=1)
    for train_idx, test_idx in cv.split(np.zeros(len(panel)), dates=dates):
        assert len(set(train_idx).intersection(test_idx)) == 0
