from contextlib import asynccontextmanager

import uvicorn
from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from common.exceptions import ToClientException
from queues.producer import producer

from api.user import router as user_router
from api.message import router as message_router
from api.notifications import router as notification_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup server")
    await producer.start()
    yield
    print("Shutdown server")
    await producer.close()


ROUTES = [
    user_router,
    message_router,
    notification_router,
]


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in ROUTES:
    app.include_router(route)


@app.exception_handler(ToClientException)
async def validation_exception_handler(request: Request, exc: ToClientException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"error": "Validation Error", "message": str(exc.message)},
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )