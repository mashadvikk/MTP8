from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from mvc_calc.model import MAX_LENGTH, CalcError, Calculator


class Expression(BaseModel):
    expression: str = Field(min_length=1, max_length=MAX_LENGTH)


class Calculation(BaseModel):
    expression: str
    result: float


def create_app():
    app = FastAPI(title="Калькулятор")
    calculator = Calculator()

    @app.post("/calculations", status_code=201)
    def calculate(data: Expression) -> Calculation:
        try:
            result = calculator.calculate(data.expression)
        except CalcError as error:
            raise HTTPException(400, str(error)) from None
        return Calculation(expression=data.expression.strip(), result=result)

    @app.get("/calculations")
    def history() -> list[Calculation]:
        return [Calculation(expression=expression, result=result)
                for expression, result in calculator.history]

    @app.delete("/calculations", status_code=204)
    def clear() -> None:
        calculator.clear()

    return app
