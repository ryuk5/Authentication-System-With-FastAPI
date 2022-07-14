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
from ..schemas.user_schema import UserInSchemaForUpdate, UserScopesAdminSchema



router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@router.post('/create', response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    new_user: UserInSchema, 
    db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return user_controller.create_user(new_user, db)


@router.put('/{id}', response_model=UserOutSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user_account(
    id: int, 
    updated_user: UserInSchemaForUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return user_controller.update_user(id, updated_user, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int, db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    user_controller.delete_user(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/all', status_code=200, response_model=List[UserOutSchema])
async def get_all_users(
    db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return user_controller.get_all_users(db)


# This endpoint will fetch the the user + his permissions 
@router.get('/{id}', status_code=200, response_model=UserScopesAdminSchema)
async def get_specific_user(
    id:int, 
    db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return user_controller.get_specific_user(id, db)
