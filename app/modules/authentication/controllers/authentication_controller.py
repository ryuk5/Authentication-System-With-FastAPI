from modules.users.schemas.user_schema import UserInSchema
from database.config import get_db
from sqlalchemy.orm import Session
from modules.users.models.user_model import User
from utilities.hashing import Hash
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modules.authentication.schemas.token_schema import *
from settings.settings import settings
from modules.users.controllers.user_controller import user_controller

# from dotenv import load_dotenv
# load_dotenv()

_hash = Hash()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthenticationController():

    def _get_user(self, db: Session, username: str):
        user = db.query(User).filter(User.email == username).first()
        if not user:
            return None

        return user
        

    def _authenticate_user(self, db: Session, username: str, password: str):
        user = self._get_user(db, username)
        if not user:
            return False
        if not _hash.verify_password(password, user.password):
            return False
        return user


    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    
    async def get_current_user(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self._get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


    def generate_token(self, user: User):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self._create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


    def login_for_access_token(self, db: Session, login_form_data: OAuth2PasswordRequestForm):
        user = self._authenticate_user(db, login_form_data.username, login_form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self.generate_token(user)



    def signup(self, new_user: UserInSchema, db: Session):
        user = user_controller.create_user(new_user, db)
        return self.generate_token(user)
        

    

authentication_controller = AuthenticationController()