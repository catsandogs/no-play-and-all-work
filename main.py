from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Создаем экземпляр приложения и задаем понятное название для Swagger
app = FastAPI(
    title="DevSecOps Calculator API",
    description="Безопасный API-калькулятор с валидацией данных для CI/CD пайплайна",
    version="1.0.0"
)


# Описываем схему входных данных с помощью Pydantic.
# Это автоматически защищает API от отправки строк вместо чисел.
class CalculationRequest(BaseModel):
    num1: float = Field(..., description="Первое число (дробное или целое)")
    num2: float = Field(..., description="Второе число (дробное или целое)")
    operation: str = Field(..., description="Операция: add, sub, mul, div")


# Главный эндпоинт для расчетов
@app.post("/calculate", summary="Выполнить математическую операцию")
def calculate(data: CalculationRequest):
    # Приводим к нижнему регистру, чтобы избежать ошибок регистра
    op = data.operation.lower().strip()

    if op == "add":
        return {"result": data.num1 + data.num2}

    elif op == "sub":
        return {"result": data.num1 - data.num2}

    elif op == "mul":
        return {"result": data.num1 * data.num2}

    elif op == "div":
        # DevSecOps-практика: явная обработка критических ошибок (деление на ноль)
        if data.num2 == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is strictly forbidden!"
            )
        return {"result": data.num1 / data.num2}

    # Если передана неизвестная операция — отдаем ошибку 400 Bad Request
    raise HTTPException(
        status_code=400,
        detail=f"Unknown operation '{data.operation}'. Use: add, sub, mul, div."
    )
