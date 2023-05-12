from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    DATETIME, SmallInteger, String, types, Integer, ForeignKey,
    Boolean, Date, Text,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import MONEY
import enum
class UserRole(str, enum.Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    
SqlUserRole = types.Enum(
    UserRole,
    name="user_roles_type",
    values_callable=lambda x: [e.value for e in x]
)
    
class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(True), default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(True),
        onupdate=datetime.now(),
        default=datetime.now(),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DATETIME(True))


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(25))
    role: Mapped[str] = mapped_column(SqlUserRole)
    
class Flower(BaseModel):
    __tablename__ = "flowers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)

class Shade(BaseModel):
    __tablename__ = "shades"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    
class FlowerShade(BaseModel):
    __tablename__ = "flower_shades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flower_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shade_id: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    
class FlowerAmount(BaseModel):
    __tablename__ = "flower_amounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    sign: Mapped[bool] = mapped_column(Boolean, default=True)
    active_date: Mapped[date] = mapped_column(Date, default=date.today())
    
class FlowerPrice(BaseModel):
    __tablename__ = "flower_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=False)
    price: Mapped[float] = mapped_column(MONEY, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, default=date.today())
    end_date: Mapped[date] = mapped_column(Date, default=date(2999, 12, 31))
    
class Lot(BaseModel):
    __tablename__ = "lots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
class Deal(BaseModel):
    __tablename__ = "deals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    executed_date: Mapped[date] = mapped_column(Date, default=date.today())
    amount: Mapped[int] = mapped_column(SmallInteger, default=1)

class FlowerReview(BaseModel):
    __tablename__ = "flower_reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
class SellerReview(BaseModel):
    __tablename__ = "seller_reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)