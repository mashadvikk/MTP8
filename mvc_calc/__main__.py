import sys

from mvc_calc.controller import Controller
from mvc_calc.model import Calculator
from mvc_calc.view import ConsoleView


def main():
    if sys.argv[1:] == ["api"]:
        import uvicorn

        uvicorn.run("mvc_calc.api:create_app", factory=True, port=8000)
        return
    Controller(Calculator(), ConsoleView()).run()


if __name__ == "__main__":
    main()
