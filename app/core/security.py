from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()
SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/users/login"
# )

from fastapi.security import HTTPBearer


bearer_scheme = HTTPBearer()

def hash_password(password:str) -> str:
    """Hash a password using the recommended hashing algorithm."""
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str) -> bool:
    """Verify a password against a hashed password."""
    return password_hash.verify(password, hashed_password)


def create_access_token( user_id: int, expires_delta: timedelta | None = None):
    """Create a JWT access token."""

    expire = datetime.now(timezone.utc)

    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload={"sub":str(user_id),"exp":expire}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

