from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from utils.schemas import TokenData
from utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Dependency to validate JWT."""
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")  # JWT 标准中 'sub' 表示用户标识
        if username is None:
            raise JWTError
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )