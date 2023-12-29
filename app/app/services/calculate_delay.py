import random

import app.schemas as S
from app.repo.error import block


class CalculateDelay:
    def __init__(self, logic: str, last_blocks: list[block], params: dict):
        self.logic = logic
        self.last_blocks = last_blocks
        self.params = params

    def calculate_time(self) -> int:
        func = self.__getattribute__(self.logic)
        return int(func() * random.uniform(0.85, 1.15))

    def sum_history(self):
        params = S.CalculatorBase(**self.params)
        if self.last_blocks:
            return sum([s for _, s in self.last_blocks])
        else:
            return params.base_time

    def linear(self):
        params = S.CalculatorBase(**self.params)
        return params.base_time + len(self.last_blocks) * params.base_time
