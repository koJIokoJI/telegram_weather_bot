from sqlalchemy import BigInteger, String, ARRAY, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models import Base


class Users(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    default_city: Mapped[str] = mapped_column(String, nullable=True)
    cities: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    mailing_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
