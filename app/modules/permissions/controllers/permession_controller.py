from ..models.permission_model import Permission
from ..schemas.permission_schema import PermissionInSchema, PermissionAssignForm, PermissionsAssignForm, PermissionRemovalForm, PermissionsRemovalForm
from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.associations.user_permission_association import UserPermissionAssociation
from modules.users.models.user_model import User
from typing import List


class PermessionController():
    
    def extract_user_scopes(self, user: User):
        scopes = []
        for association in user.permissions:
            scopes.append(association.permission.permission)
        
        return scopes


    def get_all_permissions(self, db: Session):
        permissions = db.query(Permission).all()
        return permissions


    def add_permission(self, permission: PermissionInSchema, db: Session):
        new_permission = Permission(**permission.dict())
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)
        return new_permission

    
    def delete_permission(self, id: int, db: Session):
        permission = db.query(Permission).filter(Permission.id == id)

        if not permission.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with id = {id} is not found")
        
        permission.delete(synchronize_session=False)
        db.commit()

    
    def update_permission(self, id: int, updated_permission: PermissionInSchema, db: Session):
        existing_permission_quey = db.query(Permission).filter(Permission.id == id)
        existing_permission = existing_permission_quey.first()
        if not existing_permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with id = {id} is not found")

        if existing_permission.permission != updated_permission.permission:
            permission_name_verif = db.query(Permission).filter(Permission.permission == updated_permission.permission).first()
            if permission_name_verif:
                raise HTTPException(status_code=400, detail=f"Permission with the name = {updated_permission.permission} already exists")
            else:
                existing_permission_quey.update(updated_permission.dict())
                db.commit()
        else:
            existing_permission_quey.update(updated_permission.dict())
            db.commit()

        

        output = existing_permission_quey.first()

        return output


    def assign_permission(self, permission_assign_form: PermissionAssignForm, db: Session):
            
        user = db.query(User).filter(User.id == permission_assign_form.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {permission_assign_form.user_id} is not found")

        permission = db.query(Permission).filter(Permission.id == permission_assign_form.permission_id).first()
        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with id = {permission_assign_form.permission_id} is not found")

        association = UserPermissionAssociation()
        association.permission = permission
        user.permissions.append(association)

        db.commit()

        return 'success'


    def assign_permissions(self, permissions_assign_form: PermissionsAssignForm, db: Session):
        user = db.query(User).filter(User.id == permissions_assign_form.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {permissions_assign_form.user_id} is not found")

        permissions = db.query(Permission).filter(Permission.id.in_(permissions_assign_form.permissions_ids))
        for permission in permissions.all():
            association = UserPermissionAssociation()
            association.permission = permission
            user.permissions.append(association)

        db.commit()

        return 'success'


    def remove_permission(self, permission_removal_form: PermissionRemovalForm, db: Session):
        assoc_row = db.query(UserPermissionAssociation).filter(and_(UserPermissionAssociation.user_id == permission_removal_form.user_id, UserPermissionAssociation.permission_id == permission_removal_form.permission_id))
        if not assoc_row.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {permission_removal_form.user_id} don't possesse the permission with the id = {permission_removal_form.permission_id}")

        assoc_row.delete(synchronize_session=False)
        db.commit()

        return {'msg': 'Operation done successfully'}


    def remove_permissions(self, permissions_removal_form: PermissionsRemovalForm, db: Session):
        assoc_removal_query = db.query(UserPermissionAssociation).filter(and_(UserPermissionAssociation.user_id == permissions_removal_form.user_id, UserPermissionAssociation.permission_id.in_(permissions_removal_form.permissions_ids)))
        if assoc_removal_query.count() > 0:
            assoc_removal_query.delete(synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=400, detail=f"Invalid input for permissions removal")
        
        return {'msg': 'Operation done successfully'}

        


permession_controller = PermessionController()