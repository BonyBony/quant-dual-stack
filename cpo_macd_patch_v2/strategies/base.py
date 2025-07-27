from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class BaseParams:
    pass

class IStrategy(ABC):
    @abstractmethod
    def run_day(self, df, params: BaseParams) -> float:
        ...
