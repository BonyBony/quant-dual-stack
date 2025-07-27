import pandas as pd
from typing import List, Dict, Any
from .base import IConditionalOptimizer
from models.base import IRegressor

class ConditionalParamOptimizer(IConditionalOptimizer):
    def __init__(self, model: IRegressor, param_grid: List[Dict[str, Any]]):
        self.model = model
        self.param_grid = param_grid
        self._trained = False

    def fit(self, X: pd.DataFrame, y):
        self.model.fit(X, y)
        self._trained = True
        return self

    def predict_params(self, X_today: pd.Series) -> Dict[str, Any]:
        assert self._trained, "Call fit first"
        rows = [pd.concat([X_today, pd.Series(p)]) for p in self.param_grid]
        Xc = pd.DataFrame(rows)
        preds = self.model.predict(Xc)
        best_idx = preds.argmax()
        return self.param_grid[best_idx]
