import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from events.models import Event
from events.redis_publisher import RedisEventPublisher
from gateway.auth import require_jwt_auth

logger = logging.getLogger("uvicorn.access")
router = APIRouter()


def call_api_gateway(request: Request):
    portal_id = request.path_params["portal_id"]
    print(request.path_params)
    if portal_id == str(1):
        raise RedirectStudentPortalException()
    elif portal_id == str(2):
        raise RedirectFacultyPortalException()
    elif portal_id == str(3):
        raise RedirectLibraryPortalException()


class RedirectStudentPortalException(Exception):
    pass


class RedirectFacultyPortalException(Exception):
    pass


class RedirectLibraryPortalException(Exception):
    pass


@router.post("/event/book/reserve")
def reserve_book_event(
    user=Depends(require_jwt_auth), student_id: str = None, book_id: str = None
):
    """
    Secure endpoint to publish a BookReserved event to Redis.
    Requires JWT authentication (bearer-only).
    """
    if not student_id or not book_id:
        raise HTTPException(
            status_code=400, detail="student_id and book_id are required"
        )
    event = Event.create(
        type="BookReserved", payload={"student_id": student_id, "book_id": book_id}
    )
    publisher = RedisEventPublisher(redis_url="redis://localhost:6379/0")
    publisher.publish("book.reserved", event)
    return {"status": "event published", "event": event.dict()}
