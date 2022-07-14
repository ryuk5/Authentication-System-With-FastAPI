from pydantic import BaseModel, constr
from typing import List, Optional


class BasePermissionSchema(BaseModel):
    permission: constr(regex=r'^[A-Z]+$', max_length=50)
    description: Optional[str] = None


class PermissionInSchema(BasePermissionSchema):
    pass


class PermissionOutSchema(BasePermissionSchema):
    id: int

    class Config():
        orm_mode = True


class BasePermissionManipulationForm(BaseModel):
    user_id: int
    permission_id: int


class BasePermissionsManipulationForm(BaseModel):
    user_id: int
    permissions_ids: List[int]


class PermissionAssignForm(BasePermissionManipulationForm):
    pass


class PermissionRemovalForm(BasePermissionManipulationForm):
    pass


class PermissionsAssignForm(BasePermissionsManipulationForm):
    pass

class PermissionsRemovalForm(BasePermissionsManipulationForm):
    pass