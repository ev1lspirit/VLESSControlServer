from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials

from source.api.auth.schema import LoginResponse
from source.utils.auth_utils import check_basic_auth, generate_jwt_for_user, check_jwt_auth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login_handler(credentials: HTTPBasicCredentials = Depends(check_basic_auth)):
    return LoginResponse(token=generate_jwt_for_user(credentials.username))

