import pytest

from mvc_calc.model import CalcError, calculate


@pytest.mark.parametrize("text, result", [
    ("2+3", 5), ("7 - 10", -3), ("4*2.5", 10), ("9/4", 2.25), ("42", 42)])
def test_one_operation(text, result):
    assert calculate(text) == result


@pytest.mark.parametrize("text, result", [
    ("2+3*4", 14), ("(2+3)*4", 20), ("10-4-3", 3), ("100/10/2", 5),
    ("2*(3+(4-1))", 12)])
def test_priority_and_brackets(text, result):
    assert calculate(text) == result


@pytest.mark.parametrize("text, result", [
    ("-5+2", -3), ("3*-2", -6), ("-(2+3)", -5), ("--4", 4), ("+7", 7)])
def test_unary_sign(text, result):
    assert calculate(text) == result


@pytest.mark.parametrize("text, result", [
    ("2^10", 1024), ("2^3^2", 512), ("-2^2", -4), ("2^-1", 0.5)])
def test_power(text, result):
    assert calculate(text) == result


def test_comma_is_decimal_separator():
    assert calculate("1,5+1,5") == 3


@pytest.mark.parametrize("text, message", [
    ("", "пустое выражение"),
    ("1/0", "деление на ноль"),
    ("2+", "выражение не закончено"),
    ("(1+2", "не хватает закрывающей скобки"),
    ("1+2)", "лишний символ «)»"),
    ("2 3", "лишний символ «3»"),
    ("2+a", "недопустимый символ «a»"),
    ("1..2", "недопустимый символ «.»"),
    ("*2", "недопустимый символ «*»"),
    ("(0-8)^0.5", "нет действительного результата"),
    ("9^999^9", "слишком большое число"),
])
def test_errors(text, message):
    with pytest.raises(CalcError) as error:
        calculate(text)
    assert str(error.value) == message
