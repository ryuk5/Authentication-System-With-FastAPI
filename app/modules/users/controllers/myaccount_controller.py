from ..models.user_model import User
from sqlalchemy.orm import Session
from modules.permissions.controllers.permession_controller import permession_controller
from ..schemas.user_schema import UserInSchemaForUpdate

class MyAccountController():

    def update_my_account(self, current_user: User, new_user_info: UserInSchemaForUpdate, db: Session):
        new_user_info_dict = new_user_info.dict()
        for attr in new_user_info_dict:
            setattr(current_user, attr, new_user_info_dict[attr])

        db.commit()

        new_current_user = db.query(User).filter(User.id == current_user.id).first()

        return new_current_user


    def get_myaccount_info(self, current_user: User):
        return {
            **vars(current_user), 
            'scopes': permession_controller.extract_user_scopes(current_user)
        }


myaccount_controller = MyAccountController()