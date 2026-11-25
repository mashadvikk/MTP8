import pytest

from mvc_calc.model import MAX_LENGTH, CalcError, calculate


@pytest.mark.parametrize("text", ["(" * 5000, "-" * 5000 + "1",
                                  "1" * (MAX_LENGTH + 1)])
def test_long_expression_is_rejected(text):
    with pytest.raises(CalcError, match="слишком длинное выражение"):
        calculate(text)


def test_longest_allowed_nesting():
    depth = (MAX_LENGTH - 1) // 2
    assert calculate("(" * depth + "1" + ")" * depth) == 1
    assert calculate("-" * (MAX_LENGTH - 1) + "1") == -1
