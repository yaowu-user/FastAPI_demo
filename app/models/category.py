from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship


from app.database import Base

if TYPE_CHECKING:
    from app.models.product import Product


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"comment": "分类表"}

    name: Mapped[str] = mapped_column(
        String(50), nullable=False,unique=True, comment="分类名称"
    )

    products: Mapped[list["Product"]] = relationship(back_populates="category")