from ..schemas.permission_schema import PermissionInSchema, PermissionOutSchema, PermissionAssignForm, PermissionsAssignForm, PermissionRemovalForm, PermissionsRemovalForm
from database.config import get_db
from fastapi import APIRouter, Depends, status, Response, Security
from modules.users.models.user_model import User
from typing import List
from sqlalchemy.orm import Session

from ..controllers.permession_controller import permession_controller
from modules.authentication.controllers.scopes_authentication_controller import scopes_authentication_controller


router = APIRouter(
    prefix='/permission',
    tags=['Permissions']
)


@router.get('/all', status_code=200, response_model=List[PermissionOutSchema])
def get_all_permissions(db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.get_all_permissions(db)



@router.post('/', status_code=status.HTTP_201_CREATED)
def add_permission(permission: PermissionInSchema, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
   return permession_controller.add_permission(permission, db)



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(id: int, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
   permession_controller.delete_permission(id, db)
   return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_permission(id: int, updated_permission: PermissionInSchema, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.update_permission(id, updated_permission, db)


@router.post('/assign', status_code=status.HTTP_201_CREATED)
def assign_permission(permission_assign_form: PermissionAssignForm, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.assign_permission(permission_assign_form, db)


@router.post('/mass_assign', status_code=status.HTTP_201_CREATED)
def assign_permissions(permissions_assign_form: PermissionsAssignForm, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.assign_permissions(permissions_assign_form, db)


@router.post('/remove', status_code=200)
def remove_permission(permission_removal_form: PermissionRemovalForm, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.remove_permission(permission_removal_form, db)


@router.post('/mass_remove', status_code=200)
def remove_permissions(permissions_removal_form: PermissionsRemovalForm, db: Session = Depends(get_db), current_user: User = Security(scopes_authentication_controller.get_current_user, scopes=["ADMIN"])):
    return permession_controller.remove_permissions(permissions_removal_form, db)