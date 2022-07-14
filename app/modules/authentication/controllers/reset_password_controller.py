from datetime import datetime, timedelta
from settings.settings import settings
from jose import jwt
from typing import Optional
from sqlalchemy.orm import Session
from modules.users.controllers.user_controller import user_controller
from fastapi import HTTPException, BackgroundTasks
from utilities.email_sender import email_sender
from .. schemas.reset_password_schema import ResetPasswordSchema
from utilities.hashing import Hash

_hash = Hash()

class ResetPasswordController():
    
    def __generate_password_reset_token(self, email: str) -> str:
        delta = timedelta(minutes=settings.email_reset_token_expire_minutes)
        now = datetime.utcnow()
        expires = now + delta
        encoded_jwt = jwt.encode(
            {"exp": expires, "nbf": now, "sub": email}, settings.secret_key, algorithm=settings.algorithm,
        )
        return encoded_jwt

    
    def __verify_password_reset_token(self, token: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return decoded_token["sub"]
        except jwt.JWTError:
            return None



    def recover_password(self, email: str, db: Session, background_tasks: BackgroundTasks = None) :
        user = user_controller.get_user_by_email(email, db)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system.",
            )
        password_reset_token = self.__generate_password_reset_token(email=email)
        if background_tasks is None:
            email_sender.send_email_async('FastAPI Authentication System Password Recovery', user.email, {'token': password_reset_token, 'host': 'localhost:5000'}, 'password_reset.html')
        else:
            email_sender.send_email_background(background_tasks, 'FastAPI Authentication System Password Recovery', user.email, {'token': password_reset_token, 'host': 'localhost:5000'}, 'password_reset.html')
        
        return {"msg": "Password recovery email sent"}


    def reset_password(self, reset_pwd_req_body: ResetPasswordSchema, db: Session):
        email = self.__verify_password_reset_token(reset_pwd_req_body.token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = user_controller.get_user_by_email(email, db)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system.",
            )
        
        hashed_password = _hash.get_password_hash(reset_pwd_req_body.new_password)    
        user.password = hashed_password
        db.add(user)
        db.commit()
        return {"msg": "Password updated successfully"}
    
    


reset_password_controller = ResetPasswordController()