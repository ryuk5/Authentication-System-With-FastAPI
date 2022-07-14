from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from database.config import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, unique=True, index=True) 
    description = Column(Text, nullable=True)

    users = relationship("UserPermissionAssociation", back_populates="permission")

    

    