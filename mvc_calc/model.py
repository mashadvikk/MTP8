import re

TOKEN = re.compile(r"\d+(?:[.,]\d+)?|[-+*/^()]")
MAX_VALUE = 1e100


class CalcError(Exception):
    pass


def split(text):
    tokens = []
    position = 0
    while position < len(text):
        if text[position].isspace():
            position += 1
            continue
        match = TOKEN.match(text, position)
        if match is None:
            raise CalcError(f"недопустимый символ «{text[position]}»")
        tokens.append(match.group())
        position = match.end()
    return tokens


def checked(value):
    if isinstance(value, complex):
        raise CalcError("нет действительного результата")
    if abs(value) > MAX_VALUE:
        raise CalcError("слишком большое число")
    return value


def divide(left, right):
    if right == 0:
        raise CalcError("деление на ноль")
    return left / right


def power(left, right):
    try:
        return float(left) ** right
    except ZeroDivisionError:
        raise CalcError("деление на ноль") from None
    except OverflowError:
        raise CalcError("слишком большое число") from None


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def take(self):
        token = self.peek()
        self.index += 1
        return token

    def parse(self):
        value = self.sum()
        if self.peek() is not None:
            raise CalcError(f"лишний символ «{self.peek()}»")
        return value

    def sum(self):
        value = self.product()
        while self.peek() in ("+", "-"):
            if self.take() == "+":
                value = checked(value + self.product())
            else:
                value = checked(value - self.product())
        return value

    def product(self):
        value = self.unary()
        while self.peek() in ("*", "/"):
            if self.take() == "*":
                value = checked(value * self.unary())
            else:
                value = checked(divide(value, self.unary()))
        return value

    def unary(self):
        if self.peek() == "-":
            self.take()
            return -self.unary()
        if self.peek() == "+":
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        value = self.atom()
        if self.peek() == "^":
            self.take()
            return checked(power(value, self.unary()))
        return value

    def atom(self):
        token = self.take()
        if token is None:
            raise CalcError("выражение не закончено")
        if token == "(":
            value = self.sum()
            if self.take() != ")":
                raise CalcError("не хватает закрывающей скобки")
            return value
        if not token[0].isdigit():
            raise CalcError(f"недопустимый символ «{token}»")
        return checked(float(token.replace(",", ".")))


def calculate(text):
    tokens = split(text)
    if not tokens:
        raise CalcError("пустое выражение")
    return Parser(tokens).parse()
