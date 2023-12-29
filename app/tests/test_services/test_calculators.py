from collections import namedtuple
from datetime import datetime

from app.services import CalculateDelay


def test_calc_linear():
    block = namedtuple("Block", ["date", "sleep"])
    times = [block(date=datetime.now(), sleep=0) for _ in range(5)]
    calculator = CalculateDelay("linear", times, {})
    result = calculator.linear()
    # 300 + 5 * 300
    assert result == 1800


def test_calc_linear_params():
    block = namedtuple("Block", ["date", "sleep"])
    times = [block(date=datetime.now(), sleep=0) for _ in range(5)]
    calculator = CalculateDelay("linear", times, {"base_time": 100})
    result = calculator.linear()
    # 100 + 5 * 100 = 600
    assert result == 600


def test_calc_history_sum():
    block = namedtuple("Block", ["date", "sleep"])
    times = [block(date=datetime.now(), sleep=i*100) for i in range(5)]
    calculator = CalculateDelay("linear", times, {})
    result = calculator.sum_history()
    # 0, 100, 200, 300, 400 = 1000 just sum
    assert result == 1000


def test_calc_history_sum_emtpy():
    times = []


def test_calc_is_int():
    calculator = CalculateDelay("linear", [], {"base_time": 100})
    result = calculator.calculate_time()
    assert isinstance(result, int)


def test_calc_randomizer():
    calculator = CalculateDelay("linear", [], {})
    data = set()
    for _ in range(20):
        data.add(calculator.calculate_time())
    assert len(data) > 15
