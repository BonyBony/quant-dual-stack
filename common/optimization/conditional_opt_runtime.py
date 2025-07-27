import pandas as pd
import numpy as np

class ConditionalParamRuntime:
    def __init__(self, model, param_grid, feature_cols):
        self.model = model
        self.param_grid = param_grid
        self.feature_cols = feature_cols

    def pick(self, feat_s: pd.Series):
        rows = [pd.concat([feat_s, pd.Series(p)]) for p in self.param_grid]
        Xc = pd.DataFrame(rows)[self.feature_cols]
        preds = self.model.predict(Xc)
        return self.param_grid[int(np.argmax(preds))]
