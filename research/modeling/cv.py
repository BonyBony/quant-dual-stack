"""Time-aware cross-validation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Sequence, Tuple

import numpy as np
import pandas as pd


def _to_datetime_series(values: Sequence) -> pd.Series:
    return pd.Series(pd.to_datetime(values), name="date")


@dataclass
class PurgedKFoldEmbargo:
    """Purged K-Fold with embargo for daily cross-sectional datasets."""

    n_splits: int = 5
    embargo: int = 5

    def __post_init__(self) -> None:
        if self.n_splits < 2:
            raise ValueError("n_splits must be at least 2")
        if self.embargo < 0:
            raise ValueError("embargo must be non-negative")

    def split(
        self,
        X: Sequence | pd.DataFrame | pd.Series,
        y: Sequence | None = None,
        dates: Sequence | None = None,
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        date_index = self._extract_dates(X, dates)
        unique_dates = pd.Index(sorted(date_index.unique()))
        n_dates = len(unique_dates)
        if n_dates < self.n_splits:
            raise ValueError("Not enough unique dates for the requested splits")

        fold_sizes = self._fold_sizes(n_dates)
        pointer = 0
        for size in fold_sizes:
            test_start = pointer
            test_end = pointer + size
            test_dates = unique_dates[test_start:test_end]

            test_mask = date_index.isin(test_dates)
            train_mask = ~test_mask

            purge_start = max(0, test_start - self.embargo)
            purge_end = min(n_dates, test_end + self.embargo)
            excluded = unique_dates[purge_start:purge_end]
            if len(excluded):
                train_mask &= ~date_index.isin(excluded)

            yield np.where(train_mask)[0], np.where(test_mask)[0]
            pointer = test_end

    def get_n_splits(self, X: Sequence | None = None, y: Sequence | None = None, dates: Sequence | None = None) -> int:
        return self.n_splits

    # ------------------------------------------------------------------
    def _extract_dates(self, X: Sequence | pd.DataFrame | pd.Series, dates: Sequence | None) -> pd.Series:
        if dates is not None:
            return _to_datetime_series(dates)

        if isinstance(X, (pd.DataFrame, pd.Series)):
            idx = X.index
            if isinstance(idx, pd.MultiIndex):
                if "date" in idx.names:
                    return _to_datetime_series(idx.get_level_values("date"))
                return _to_datetime_series(idx.get_level_values(0))
            return _to_datetime_series(idx)
        raise ValueError("dates must be supplied when X is not a pandas object")

    def _fold_sizes(self, n_dates: int) -> list[int]:
        base = n_dates // self.n_splits
        remainder = n_dates % self.n_splits
        sizes = [base + 1 if i < remainder else base for i in range(self.n_splits)]
        return sizes
