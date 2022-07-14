from ..models.user_model import User
from typing import List
from database.config import get_db
from fastapi import APIRouter, Depends, Security, status, Response
from ..schemas.user_schema import UserInSchema, UserOutSchema
from ..controllers.user_controller import user_controller
# from modules.authentication.controllers.authentication_controller import authentication_controller
from modules.authentication.controllers.scopes_authentication_controller import scopes_authentication_controller
from sqlalchemy.orm import Session
from modules.authentication.schemas.token_schema import Token

from . import user_admin_routes, user_myaccount_routes


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


router.include_router(user_admin_routes.router)
router.include_router(user_myaccount_routes.router)


# @router.get("/me")
# async def login_for_access_token(current_user = Depends(scopes_authentication_controller.get_current_user)):
#     print('__________')
#     print('the user permessions')
#     print(current_user.permissions)
#     # for association in current_user.permissions:
#     #     print(association.permission.permission)
#     #     print("----")

#     return current_user


# @router.get('/allowed')
# def allowed(current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["PERM1", "PERM3"])):
#     return 'you are allowed to visit this endpoint'


# @router.get('/not_allowed')
# def not_allowed(current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["items"])):
#     return 'Endpoint is not allowed for you'



# @router.post("/me")
# async def add_user(db: Session = Depends(get_db)):
#     user = User(lastname="hamma", firstname="hamma", email="hamma@gmail.com", password=_hash.get_password_hash('hamma'))
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return user

# @router.get('/test')
# async def test(current_user = Depends(authentication_controller.get_current_user)):
#     return 'test'