import itertools, random
from typing import Dict, List, Any
from optimization.base import IParamTuner

class GridTuner(IParamTuner):
    def __init__(self, grid: Dict[str, List[Any]]):
        self.grid_items = list(itertools.product(*grid.values()))
        self.keys = list(grid.keys())
        self._i = 0
    def sample(self):
        if self._i >= len(self.grid_items):
            raise StopIteration
        vals = self.grid_items[self._i]
        self._i += 1
        return dict(zip(self.keys, vals))

class RandomTuner(IParamTuner):
    def __init__(self, space: Dict[str, List[Any]], n_samples: int):
        self.space = space
        self.n = n_samples
    def sample(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return {k: random.choice(v) for k, v in self.space.items()}
