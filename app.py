from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import RequestValidationError
from Exceptions import BusinessLogicException
from routers import imports

app = FastAPI()
app.include_router(imports.router)

@app.exception_handler(RequestValidationError)
async def handler_validation_error(request: Request, exc: RequestValidationError):
    return Response(status_code=400)

@app.exception_handler(BusinessLogicException)
async def handler_validation_error(request: Request, exc: BusinessLogicException):
    return Response(status_code=400)


