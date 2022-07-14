from ..schemas.user_schema import UserInSchema, UserInSchemaForUpdate
from ..models.user_model import User
from sqlalchemy.orm import Session
from utilities.hashing import Hash
from fastapi import status, HTTPException
from modules.permissions.controllers.permession_controller import permession_controller

_hash = Hash()

class UserController():

    def get_user_by_email(self, email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None

        return user

        
    def create_user(self, new_user: UserInSchema, db: Session):
        user = self.get_user_by_email(new_user.email, db)
        if user:
            raise HTTPException(status_code=400, detail=f"User with the email provided already exists")

        dict_new_user = new_user.dict()
        dict_new_user['password'] = _hash.get_password_hash(dict_new_user['password'])
        user = User(**dict_new_user)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user



    def update_user(self, id: int, updated_user: UserInSchemaForUpdate, db: Session):
        user = db.query(User).filter(User.id == id)
        if not user.first():
            raise HTTPException(status_code=404, detail=f"User with the id = {id} is not found")

        user.update(**updated_user.dict())
        db.commit()

        return user.first()

        
    def delete_user(self, id: int, db: Session):
        user = db.query(User).filter(User.id == id)

        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} is not found")
        
        user.delete(synchronize_session=False)
        db.commit()


    def get_all_users(self, db: Session):
        users = db.query(User).all()
        return users


    def get_specific_user(self, id: int, db: Session):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} is not found")

        return {
            **vars(user),
            "scopes": permession_controller.extract_user_scopes(user)
        }





user_controller = UserController()