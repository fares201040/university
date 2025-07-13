from uuid import uuid4

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger

from controller import university
from faculty_mgt import faculty_main
from gateway.api_router import (
    RedirectFacultyPortalException,
    RedirectLibraryPortalException,
    RedirectStudentPortalException,
    call_api_gateway,
)
from gateway.auth import add_cors, require_jwt_auth
from gateway.auth import router as auth_router
from library_mgt import library_main
from student_mgt import student_main

app = FastAPI()
app.include_router(
    university.router, dependencies=[Depends(call_api_gateway)], prefix="/ch04"
)
app.include_router(auth_router, prefix="/auth")
logger.add(
    "info.log",
    format="Log: [{extra[log_id]}: {time} - {level} - {message} ",
    level="INFO",
    enqueue=True,
)

add_cors(app)


@app.middleware("http")
async def log_middleware(request: Request, call_next):

    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        logger.info("Request to access " + request.url.path)
        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error(f"Request to " + request.url.path + " failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        finally:
            logger.info("Successfully accessed " + request.url.path)
            return response


@app.exception_handler(RedirectStudentPortalException)
def exception_handler_student(
    request: Request, exc: RedirectStudentPortalException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/ch04/student/index")


@app.exception_handler(RedirectFacultyPortalException)
def exception_handler_faculty(
    request: Request, exc: RedirectFacultyPortalException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/ch04/faculty/index")


@app.exception_handler(RedirectLibraryPortalException)
def exception_handler_library(
    request: Request, exc: RedirectLibraryPortalException
) -> Response:
    return RedirectResponse(url="http://localhost:8000/ch04/library/index")


@app.get("/secure-ping")
def secure_ping(payload=Depends(require_jwt_auth)):
    """A protected endpoint that requires a valid JWT from Keycloak."""
    return {"message": "Authenticated!", "user": payload}


app.mount("/ch04/student", student_main.student_app)
app.mount("/ch04/faculty", faculty_main.faculty_app)
app.mount("/ch04/library", library_main.library_app)
