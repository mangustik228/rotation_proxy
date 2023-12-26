from datetime import datetime
import app.schemas as S
import random


class CalculateDelay:
    def __init__(self, logic: str, last_blocks: list[datetime], params: dict):
        self.logic = logic
        self.last_blocks = last_blocks
        self.now = datetime.now()
        self.params = params

    def linear(self):
        params = S.CalculatorLinear(**self.params)
        seconds_to_sleep = params.base_time + \
            len(self.last_blocks) * params.increment

    def exponential(self):
        params = S.CalculatorExponential(**self.params)
        seconds_to_sleep = params.base_time * \
            (params.multiplier ** len(self.last_blocks))

    def frequency(self):
        params = S.CalculatorFrequency(**self.params)

    def calculate_time(self, **kwargs) -> int:
        func = self.__getattribute__(self.logic)
        return func()
