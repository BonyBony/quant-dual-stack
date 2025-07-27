from abc import ABC, abstractmethod
from typing import Dict, Any

class IParamTuner(ABC):
    @abstractmethod
    def sample(self) -> Dict[str, Any]:
        ...

class IConditionalOptimizer(ABC):
    @abstractmethod
    def fit(self, X, y): ...
    @abstractmethod
    def predict_params(self, X_today) -> Dict[str, Any]: ...
