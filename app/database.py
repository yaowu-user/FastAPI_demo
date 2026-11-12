from datetime import datetime
from sqlalchemy import DateTime, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from app.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,autoincrement=True,sort_order=-1,comment = "主键ID"
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime,nullable=False,default=datetime.now, comment="创建时间"
    )
