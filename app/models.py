from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    name: Mapped[str]
    code: Mapped[str]
    appeals: Mapped[list["Appeal"]] = relationship("Appeal", back_populates="user")


class Appeal(Base):
    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    message: Mapped[str]
    email: Mapped[str]
    status: Mapped[str]
    datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[User] = relationship("User", back_populates="appeals", lazy="joined")
