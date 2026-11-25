import pytest

from mvc_calc.model import CalcError, Calculator


@pytest.fixture
def calculator():
    return Calculator(limit=3)


def test_history_is_empty_at_start(calculator):
    assert calculator.history == []


def test_result_is_saved(calculator):
    assert calculator.calculate(" 2+2 ") == 4
    assert calculator.history == [("2+2", 4)]


def test_error_is_not_saved(calculator):
    with pytest.raises(CalcError):
        calculator.calculate("1/0")
    assert calculator.history == []


def test_only_last_records_are_kept(calculator):
    for number in range(5):
        calculator.calculate(f"{number}*2")
    assert calculator.history == [("2*2", 4), ("3*2", 6), ("4*2", 8)]


def test_ans_is_previous_result(calculator):
    calculator.calculate("10/4")
    assert calculator.calculate("ans*2") == 5


def test_ans_can_be_negative(calculator):
    calculator.calculate("2-5")
    assert calculator.calculate("ans^2") == 9


def test_ans_without_history(calculator):
    with pytest.raises(CalcError, match="нет предыдущего результата"):
        calculator.calculate("ans+1")


def test_history_copy_is_safe(calculator):
    calculator.calculate("1+1")
    calculator.history.clear()
    assert len(calculator.history) == 1


def test_clear(calculator):
    calculator.calculate("1+1")
    calculator.clear()
    assert calculator.history == []
