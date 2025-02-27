import logging
from datetime import datetime, timedelta
import bcrypt
from authlib.jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from config import Config

logger = logging.getLogger(__name__)
basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()


async def check_basic_auth(credentials: HTTPBasicCredentials = Depends(basic_auth)) -> HTTPBasicCredentials:
    usernames_equal = credentials.username == Config.CONTROL_AUTH_LOGIN
    passwords_equal = bcrypt.checkpw(
        password=credentials.password.encode('utf-8'),
        hashed_password=Config.CONTROL_AUTH_PASS_HASH.encode('utf-8')
    )
    if not all((usernames_equal, passwords_equal)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="passwrods don't match"
        )
    return credentials


def generate_jwt_for_user(session_id: str) -> str:
    """
    Генерирует jwt токен по сессии пользователя.
    """
    now = datetime.now()
    payload = {
        "session_id": session_id,
        "iat": now,
        "exp": now + timedelta(minutes=Config.SESSION_LIFETIME_MIN),
    }

    # Генерация JWT токена
    jwt_token = jwt.encode(header={"alg": "RS256"},
                           payload=payload,
                           key=Config.PRIVATE_KEY)
    return jwt_token.decode('utf-8')


async def get_jwt_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_auth),
) -> dict:
    """
    Вытаскивает payload из токена пользователя. Возвращает payload в виде dict.
    """
    try:
        jwt_token = jwt.decode(
            s=credentials.credentials,
            key=Config.PUBLIC_KEY)
    except Exception as e:
        logger.error("Invalid token given: %s", str(e))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return jwt_token


async def check_jwt_auth(jwt_payload: dict = Depends(get_jwt_payload)):
    session = jwt_payload.get("session_id") == Config.CONTROL_AUTH_LOGIN
    if not session:
        logger.error("Session not found.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session