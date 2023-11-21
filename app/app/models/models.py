from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from app.db_postgres import Base


class ProxyType(Base):
    __tablename__ = "type"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)


class Proxy(Base):
    __tablename__ = "proxy"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    server: Mapped[str | None]
    username: Mapped[str]
    password: Mapped[str]
    port: Mapped[int]
    expire: Mapped[datetime] = mapped_column(DateTime)
    service: Mapped[str]
    location: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"))
    errors: Mapped[list["Error"] | None] = relationship(back_populates="proxy")
    __table_args__ = (UniqueConstraint(
        'username',
        'password',
        'port',
        'server',
        'expire',
        name='unique_value'),)


class Error(Base):
    __tablename__ = "error"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    proxy_id: Mapped[int] = mapped_column(ForeignKey("proxy.id"))
    proxy = relationship("Proxy", back_populates="errors")
