from fastapi import APIRouter, Depends, Security, status, Response
from database.config import get_db
from sqlalchemy.orm import Session
from modules.authentication.controllers.scopes_authentication_controller import scopes_authentication_controller
from ..models.user_model import User
from ..controllers.user_controller import user_controller
from ..controllers.myaccount_controller import myaccount_controller
from ..schemas.user_schema import UserScopesSchema, UserInSchemaForUpdate


router = APIRouter(
    prefix='/myaccount',
    tags=['My Account']
)

# Add response model here
@router.get('/', response_model=UserScopesSchema)
async def get_my_account_info(
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=[])):
    return myaccount_controller.get_myaccount_info(current_user)


@router.put('/')
async def update_my_account_info(
    new_user_info: UserInSchemaForUpdate,
    db: Session = Depends(get_db), 
    current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=[])):
    return myaccount_controller.update_my_account(current_user, new_user_info, db)
