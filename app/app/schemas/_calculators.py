from pydantic import BaseModel


class CalculatorBase(BaseModel):
    base_time: int = 600
