from datetime import datetime
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from app.db_postgres import Base


class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    proxies: Mapped[List["Proxy"]] = relationship(back_populates="location")


class ProxyType(Base):
    __tablename__ = "type"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    proxies: Mapped[List["Proxy"]] = relationship(back_populates="proxy_type")


class Service(Base):
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    proxies: Mapped[List["Proxy"]] = relationship(back_populates="service")
    description: Mapped[str] = mapped_column(nullable=True)


class Error(Base):
    __tablename__ = "error"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    proxy_id: Mapped[int] = mapped_column(ForeignKey("proxy.id"))
    proxy: Mapped["Proxy"] = relationship(back_populates="errors")


class Proxy(Base):
    __tablename__ = "proxy"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    server: Mapped[str | None]
    username: Mapped[str]
    password: Mapped[str]
    port: Mapped[int]
    expire: Mapped[datetime] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)

    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id"), default=1)
    location: Mapped["Location"] = relationship(back_populates="proxies")

    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    service: Mapped["Service"] = relationship(back_populates="proxies")

    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"), default=1)
    proxy_type: Mapped["ProxyType"] = relationship(back_populates="proxies")

    errors: Mapped[list["Error"] | None] = relationship(back_populates="proxy")

    __table_args__ = (UniqueConstraint(
        'username',
        'password',
        'port',
        'server',
        'expire',
        name='unique_value'),)
