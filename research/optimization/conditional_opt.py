import pandas as pd
from typing import List, Dict, Any
from common.models.base import IRegressor

class ConditionalParamOptimizer:
    def __init__(self, model: IRegressor, param_grid: List[Dict[str, Any]]):
        self.model = model
        self.param_grid = param_grid
        self._trained = False

    def fit(self, X: pd.DataFrame, y):
        self.model.fit(X, y)
        self._trained = True
        self.feature_cols = list(X.columns)
        return self

    def get_runtime_bundle(self):
        return {
            "feature_cols": self.feature_cols,
            "param_grid": self.param_grid
        }

    def predict_params(self, X_today: pd.Series) -> Dict[str, Any]:
        assert self._trained
        rows = [pd.concat([X_today, pd.Series(p)]) for p in self.param_grid]
        Xc = pd.DataFrame(rows)[self.feature_cols]
        preds = self.model.predict(Xc)
        return self.param_grid[int(preds.argmax())]
