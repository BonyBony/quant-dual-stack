from .base import IRegressor
from sklearn.ensemble import GradientBoostingRegressor

class GBRTRegressor(IRegressor):
    def __init__(self, **kwargs):
        self.model = GradientBoostingRegressor(**kwargs)
    def fit(self, X, y):
        self.model.fit(X, y)
        return self
    def predict(self, X):
        return self.model.predict(X)

REGISTRY = {
    "gbrt": GBRTRegressor,
}

def get_regressor(name: str, **kwargs) -> IRegressor:
    return REGISTRY[name](**kwargs)
