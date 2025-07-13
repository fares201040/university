import threading

from fastapi import Depends, FastAPI

from configuration.config import LibrarySettings
from events.redis_consumer import BookReservedHandler, RedisEventConsumer
from gateway.auth import require_jwt_auth
from library_mgt.controllers import admin, management

library_app = FastAPI()
library_app.include_router(admin.router)
library_app.include_router(management.router)


def build_config():
    return LibrarySettings()


@library_app.get("/index")
def index_library(config: LibrarySettings = Depends(build_config)):
    return {
        "project_name": config.application,
        "webmaster": config.webmaster,
        "created": config.created,
    }


def start_event_consumer():
    handler = BookReservedHandler()
    consumer = RedisEventConsumer(
        redis_url="redis://localhost:6379/0", channel="book.reserved", handler=handler
    )
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()


@library_app.get("/secure-library")
def secure_library(user=Depends(require_jwt_auth)):
    return {"message": "Authenticated access to library!", "user": user}


start_event_consumer()
