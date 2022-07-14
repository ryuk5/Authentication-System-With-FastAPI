from modules.users.schemas.user_schema import UserInSchema
from modules.users.controllers.user_controller import user_controller
from .authentication_controller import AuthenticationController
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database.config import get_db
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from settings.settings import settings
from ..schemas.scopes_token_schema import ScopesTokenData
from jose import JWTError, jwt
from pydantic import ValidationError
from datetime import timedelta
from modules.permissions.controllers.permession_controller import permession_controller
from modules.users.models.user_model import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="scopes_login",
    # scopes={"me": "Read information about the current user.", "items": "Read items."},
)

class ScopesAuthenticationController(AuthenticationController):
    
    async def get_current_user(self, security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = ScopesTokenData(scopes=token_scopes, username=username)
        except (JWTError, ValidationError):
            raise credentials_exception
        user = self._get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user


    def generate_token(self, user: User):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self._create_access_token(
            data={"sub": user.email, "scopes": permession_controller.extract_user_scopes(user)},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}


    def login_for_access_token(self, db: Session, login_form_data: OAuth2PasswordRequestForm):
        user = self._authenticate_user(db, login_form_data.username, login_form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        return self.generate_token(user)


    def signup(self, new_user: UserInSchema, db: Session):
        user = user_controller.create_user(new_user, db)
        return self.generate_token(user)    

scopes_authentication_controller = ScopesAuthenticationController()