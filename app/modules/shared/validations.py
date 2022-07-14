from pydantic import constr, validate_arguments, Field
from pydantic.typing import Annotated
import re

@validate_arguments
# def verify_password(password: constr(regex=r'^[^\n ]*$', min_length=8, max_length=50)) -> str:
def verify_password(password: Annotated[str, Field(regex=r'^[^\n ]*$', min_length=8, max_length=50)]) -> str:
    if re.search("^[a-zA-Z]+$", password):
        raise ValueError('The password only contain alphabetic chars')
            
    if re.search("^[0-9]+$", password):
        raise ValueError('The password only contain numbers')

    if re.search("^[^a-zA-Z0-9]+$", password):
        raise ValueError('The password only contain special characters')

    if not (re.search("[a-zA-Z]", password) and re.search("[0-9]", password) and re.search("[^a-zA-Z0-9]", password)):
        raise ValueError('The password must contain alphabetic chars, numbers and special characters')

    return password

