from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False, default="")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    warranty_reminders_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    preferred_currency: Mapped[str] = mapped_column(String, nullable=False, default="USD")
