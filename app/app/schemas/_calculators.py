from pydantic import BaseModel


class CalculatorLinear(BaseModel):
    base_time: int
    increment: int


class CalculatorExponential(BaseModel):
    base_time: int
    multiplier: int


class CalculatorFrequency(BaseModel):
    base_time: int
    max_time: int
