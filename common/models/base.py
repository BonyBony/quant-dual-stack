from abc import ABC, abstractmethod

class IRegressor(ABC):
    @abstractmethod
    def fit(self, X, y): ...
    @abstractmethod
    def predict(self, X): ...
