from mvc_calc.model import CalcError


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.commands = {"история": self.history, "очистить": self.clear}

    def run(self):
        self.view.show_help()
        while True:
            line = self.view.ask()
            if line is None or not self.handle(line):
                break
        self.view.show_bye()

    def handle(self, line):
        text = line.strip()
        command = text.lower()
        if command == "выход":
            return False
        if command in self.commands:
            self.commands[command]()
        elif text:
            self.calculate(text)
        return True

    def calculate(self, text):
        try:
            result = self.model.calculate(text)
        except CalcError as error:
            self.view.show_error(str(error))
        else:
            self.view.show_result(text, result)

    def history(self):
        self.view.show_history(self.model.history)

    def clear(self):
        self.model.clear()
        self.view.show_cleared()
