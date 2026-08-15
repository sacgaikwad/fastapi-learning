from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)
from app.dependencies.user import get_user_service
from app.models.role import UserRole

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):
    try:
        token = credentials.credentials

        #print("TOKEN:", credentials.credentials)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        return int(user_id)

    except jwt.PyJWTError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def require_roles(*allowed_roles:UserRole):
     
     def roles_checker(current_user_id:int = Depends(get_current_user), service = Depends(get_user_service)):
          print("Service Type:",type(service))
          current_user = service.get_user(current_user_id)

          if current_user.role not in allowed_roles:
               raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Insufficient permissions")
          return current_user
     return roles_checker