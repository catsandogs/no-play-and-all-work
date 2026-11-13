from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# Создаем экземпляр приложения (+ норм название для swagger)
app = FastAPI(
    title="DevSecOps Calculator API",
    description="Безопасный API-калькулятор с валида данных для ПП .",
    version="1.0.0"
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# описываем схему входных данных с Pydantic. это автоматически защищает API от отправки строк вместо чисел.
class CalculationRequest(BaseModel):
    num1: float = Field(..., description="Первое число (дробное или целое)")
    num2: float = Field(..., description="Второе число (дробное или целое)")
    operation: str = Field(..., description="Операция: add, sub, mul, div")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/calculate", summary="Выполнить математическую операцию")
def calculate(data: CalculationRequest):
    op = data.operation.lower().strip()

    if op == "add":
        return {"result": data.num1 + data.num2}

    elif op == "sub":
        return {"result": data.num1 - data.num2}

    elif op == "mul":
        return {"result": data.num1 * data.num2}

    elif op == "div":
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

@app.get("/health")
def health():
    return {"status": "ok", "version": app.version}
