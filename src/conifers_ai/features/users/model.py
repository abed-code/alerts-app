
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from conifers_ai.core.database import AppModel


class User(AppModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
