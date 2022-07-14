from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config import Base
from database.associations.user_permission_association import UserPermissionAssociation


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)

    permissions = relationship("UserPermissionAssociation", back_populates="user")

    