from pydantic import BaseModel, constr, validator
import re
from modules.shared.validations import verify_password

class ResetPasswordSchema(BaseModel):
    token: str
    # All characters except space 
    # new_password: constr(regex=r'^[^\n ]*$', min_length=8, max_length=50)
    new_password: str

    # validators
    _verify_new_password = validator('new_password', allow_reuse=True)(verify_password)

    # @validator('new_password')
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