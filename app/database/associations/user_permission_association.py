from database.config import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

class UserPermissionAssociation(Base):
    __tablename__ = 'user_permission_association'

    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    permission_id = Column(ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="users")

    # lazy="immediate"