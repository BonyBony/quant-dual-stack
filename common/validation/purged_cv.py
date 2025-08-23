# common/validation/purged_cv.py
from __future__ import annotations
from typing import Iterator, Tuple, Sequence
import numpy as np
import pandas as pd

class PurgedGroupTimeSeriesSplit:
    """
    Leakage-safe CV:
      • time-ordered folds
      • groups = e.g., dates; validation blocks are contiguous in time
      • training uses ONLY groups strictly before the validation block
      • optional embargo (in # groups) immediately before validation is dropped from train

    Parameters
    ----------
    n_splits : int
    embargo_groups : int, default 1
        Number of *group* steps to drop before the validation block.
    """

    def __init__(self, n_splits: int = 5, embargo_groups: int = 1):
        if n_splits < 2:
            raise ValueError("n_splits >= 2")
        self.n_splits = int(n_splits)
        self.embargo_groups = max(0, int(embargo_groups))

    def split(self, X, groups: Sequence, y=None) -> Iterator[Tuple[np.ndarray, np.ndarray]]:
        """
        Parameters
        ----------
        X : any
            Not used; included for sklearn compatibility.
        groups : Sequence
            Group labels aligned 1:1 with rows of X (e.g., dates).
        y : any, optional
            Not used; included for sklearn compatibility.
        """
        if groups is None:
            raise ValueError("groups must be provided (e.g., dates per row)")

        g = pd.Index(groups)
        # preserve time order as given in `groups`
        u = pd.Index(g.unique())
        n = len(u)
        if n < (self.n_splits + 1):
            # still yield a single split if possible
            self._yield_single(g, u)
            return

        # Create n_splits validation blocks (time-ordered)
        cuts = np.linspace(0, n, self.n_splits + 2, dtype=int)  # 0 .. n
        for k in range(self.n_splits):
            val_start, val_end = cuts[k + 1], cuts[k + 2]  # [start, end)
            if val_end - val_start < 1:
                continue

            # Training groups end before the embargoed zone
            train_end = max(0, val_start - self.embargo_groups)
            train_groups = set(u[:train_end])
            val_groups = set(u[val_start:val_end])

            train_idx = np.where(g.isin(train_groups))[0]
            val_idx = np.where(g.isin(val_groups))[0]
            if len(train_idx) == 0 or len(val_idx) == 0:
                continue
            yield train_idx, val_idx

    def _yield_single(self, g: pd.Index, u: pd.Index):
        """Fallback: yield one split if there are too few unique groups."""
        n = len(u)
        if n < 3:
            return
        cut = n - 1
        train_groups = set(u[: max(0, cut - self.embargo_groups)])
        val_groups = set(u[cut:])

        train_idx = np.where(g.isin(train_groups))[0]
        val_idx = np.where(g.isin(val_groups))[0]
        if len(train_idx) and len(val_idx):
            yield train_idx, val_idx
