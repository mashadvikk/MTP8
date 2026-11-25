import pytest

from mvc_calc.controller import Controller
from mvc_calc.model import Calculator
from mvc_calc.view import ConsoleView, format_number


@pytest.mark.parametrize("value, text", [
    (4.0, "4"), (0.1 + 0.2, "0.3"), (-0.0, "0"), (1 / 3, "0.3333333333"),
    (1e20, "1e+20")])
def test_format_number(value, text):
    assert format_number(value) == text


class FakeView:
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        return lambda *args: self.calls.append((name, *args))


@pytest.fixture
def view():
    return FakeView()


@pytest.fixture
def controller(view):
    return Controller(Calculator(), view)


def test_controller_shows_result(controller, view):
    assert controller.handle("2+2")
    assert view.calls == [("show_result", "2+2", 4)]


def test_controller_shows_error(controller, view):
    assert controller.handle("1/0")
    assert view.calls == [("show_error", "деление на ноль")]


def test_controller_history_and_clear(controller, view):
    controller.handle("1+1")
    controller.handle(" ИСТОРИЯ ")
    controller.handle("очистить")
    controller.handle("история")
    assert view.calls[1:] == [("show_history", [("1+1", 2)]),
                              ("show_cleared",), ("show_history", [])]


def test_controller_ignores_empty_line(controller, view):
    assert controller.handle("   ")
    assert view.calls == []


def test_controller_exit(controller, view):
    assert not controller.handle("выход")


def run(*lines):
    source = iter(lines)
    output = []

    def read(prompt):
        try:
            return next(source)
        except StopIteration:
            raise EOFError from None

    view = ConsoleView(read=read, write=output.append)
    Controller(Calculator(), view).run()
    return output


def test_whole_dialog():
    assert run("2+3", "ans*2", "1/0", "история", "выход", "9*9")[1:] == [
        "2+3 = 5", "ans*2 = 10", "Ошибка: деление на ноль",
        "1) 2+3 = 5", "2) ans*2 = 10", "До свидания!"]


def test_end_of_input_stops_program():
    assert run("история")[1:] == ["История пуста", "До свидания!"]
