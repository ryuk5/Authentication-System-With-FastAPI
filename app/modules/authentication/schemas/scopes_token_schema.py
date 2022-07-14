from .token_schema import TokenData
from typing import List

class ScopesTokenData(TokenData):
    scopes: List[str] = []
