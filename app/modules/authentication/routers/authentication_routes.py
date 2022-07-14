from fastapi import APIRouter, Depends, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.config import get_db
from modules.authentication.schemas.token_schema import Token
# from modules.authentication.controllers.authentication_controller import authentication_controller
from modules.authentication.controllers.scopes_authentication_controller import scopes_authentication_controller
from typing import Any
from ..controllers.reset_password_controller import reset_password_controller
from ..schemas.reset_password_schema import ResetPasswordSchema
from modules.users.schemas.user_schema import UserInSchema

router = APIRouter(
    tags=['Authentication']
)


# @router.post("/login", response_model=Token)
# async def login_for_access_token(db: Session = Depends(get_db), login_form_data: OAuth2PasswordRequestForm = Depends()):
#     return authentication_controller.login_for_access_token(db, login_form_data)


@router.post("/scopes_login", response_model=Token)
async def scopes_login_for_access_token(db: Session = Depends(get_db), login_form_data: OAuth2PasswordRequestForm = Depends()):
    return scopes_authentication_controller.login_for_access_token(db, login_form_data)



@router.post('/signup', response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(new_user: UserInSchema, db: Session = Depends(get_db)):
    return scopes_authentication_controller.signup(new_user, db)


@router.post("/password-recovery/{email}" """, response_model=schemas.Msg""")
def recover_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    return reset_password_controller.recover_password(email, db, background_tasks)


@router.post("/reset-password/" """, response_model=schemas.Msg""")
def reset_password(
    reset_pwd_req_body: ResetPasswordSchema,
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset password
    """
    return reset_password_controller.reset_password(reset_pwd_req_body, db)