from pydantic import BaseModel, constr, EmailStr, validator
from typing import Optional, List
import re
from modules.shared.validations import verify_password

class BaseUserSchema(BaseModel):
    firstname: constr(regex=r'^[a-zA-Z]+$', max_length=50)
    lastname: constr(regex=r'^[a-zA-Z]+$', max_length=50)


class BaseUserWithEmailSchema(BaseUserSchema):
    email: EmailStr

    
class UserInSchema(BaseUserWithEmailSchema):
    # All characters except space 
    # password: constr(regex=r'^[^\n ]*$', min_length=8, max_length=50)
    password: str

    # validators
    _verify_password = validator('password', allow_reuse=True)(verify_password)

    # @validator('password')
    # def pwd_must_contain_all_kind_of_chars(cls, v):
    #     if re.search("^[a-zA-Z]+$", v):
    #         raise ValueError('The password only contain alphabetic chars')
            
    #     if re.search("^[0-9]+$", v):
    #         raise ValueError('The password only contain numbers')

    #     if re.search("^[^a-zA-Z0-9]+$", v):
    #         raise ValueError('The password only contain special characters')

    #     if not (re.search("[a-zA-Z]", v) and re.search("[0-9]", v) and re.search("[^a-zA-Z0-9]", v)):
    #         raise ValueError('The password must contain alphabetic chars, numbers and special characters')

    #     return v



class UserOutSchema(BaseUserWithEmailSchema):
    id: int

    class Config():
        orm_mode = True


class UserScopesSchema(BaseUserWithEmailSchema):
    scopes: List[str]


class UserScopesAdminSchema(UserScopesSchema):
    id: int



class UserInSchemaForUpdate(BaseUserSchema):
    pass