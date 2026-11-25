def format_number(value):
    return f"{value + 0.0:.10g}"


class ConsoleView:
    def __init__(self, read=input, write=print):
        self._read = read
        self._write = write

    def ask(self):
        try:
            return self._read("> ")
        except EOFError:
            return None

    def show_help(self):
        self._write("Введите выражение или команду: "
                    "история, очистить, выход")

    def show_result(self, expression, result):
        self._write(f"{expression} = {format_number(result)}")

    def show_error(self, message):
        self._write(f"Ошибка: {message}")

    def show_history(self, history):
        if not history:
            self._write("История пуста")
        for number, (expression, result) in enumerate(history, 1):
            self._write(f"{number}) {expression} = {format_number(result)}")

    def show_cleared(self):
        self._write("История очищена")

    def show_bye(self):
        self._write("До свидания!")
