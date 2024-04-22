from dataclasses import dataclass
from typing import Annotated, Dict
from pydantic import BaseModel, UUID4
from litestar import Litestar, get, post
from litestar.params import Body
import uvicorn
from mcv_api.session.session import ChulaLogin
from app.utils.logging import logger

@get("/")
async def index() -> str:
    return "Up and running!"

@dataclass
class LoginCredential:
    username: str
    password: str

@dataclass
class Session:
    _token: str

@dataclass
class LoginResponse:
    success: bool
    message: str
    session: Session | None

@post("/login")
async def login_chula(
    data: Annotated[LoginCredential, Body(title="Create User", description="Create a new user.")],
) -> LoginResponse:
    try:
        try:
            client = ChulaLogin(data.username, data.password)
        except ValueError as e:
            logger.error(e)
            return LoginResponse(success=False, message=str(e), session=None)
        
        return LoginResponse(success=True, message="Login successful", session=Session(
            _token=client.csrf_token
        ))
    except Exception as e:
        logger.error(e)
        return LoginResponse(success=False, message=str(e), session=None)

# -------------- Error Handling --------------
from litestar import Litestar, MediaType, Request, Response, get
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
def plain_text_exception_handler(_: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")

    logger.error(f"Error: {detail}")
    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=status_code,
    )
    
app = Litestar(
    [index, login_chula],
    exception_handlers={HTTPException: plain_text_exception_handler},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)