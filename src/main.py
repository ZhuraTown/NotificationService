import asyncio

import uvicorn
from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

from api.managers.notification import manager_notifications
from common.exceptions import ToClientException
from config import NOTIFICATIONS_CHANNEL_NAME
from pub_sub.sub import subscriber
from queues.producer import producer

from api.user import router as user_router
from api.message import router as message_router
from api.notifications import router as notification_router
from service.notifications import broadcast_new_notifications


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup server")
    await producer.start()
    asyncio.create_task(
        broadcast_new_notifications(
            channel_name=NOTIFICATIONS_CHANNEL_NAME,
            sub=subscriber,
            ws_manager=manager_notifications,
        )
    )
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