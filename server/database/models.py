from sqlalchemy import Boolean, Integer, String, false, DateTime, BigInteger, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from database.base_model import Base, TimestampMixin
from datetime import datetime
from typing import Optional


def _now() -> datetime:
    return datetime.now()

class User(Base, TimestampMixin):
    """
    用户模型
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(255), nullable=True, comment="用户名")
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="邮箱"
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")

class File(Base, TimestampMixin):
    """
    文件模型
    """

    __tablename__ = "files"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="文件ID")
    md5: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件MD5")
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件名")
    filepath: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件路径")
    filesize: Mapped[int] = mapped_column(Integer, nullable=False, comment="文件大小")
    mimetype: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件类型")
    vectorized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false(), comment="是否已向量化")

class Client(Base, TimestampMixin):
    """
    文件模型
    """

    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="客户ID")
    email: Mapped[str] = mapped_column(String(255), nullable=False, comment="邮箱")
    mobile: Mapped[str] = mapped_column(String(255), nullable=False, comment="电话")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")

class ChatSession(Base):
    __tablename__ = "chat_session"

    id: Mapped[str] = mapped_column(PG_UUID(as_uuid=False), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AgentChatMessage(Base):
    """映射 ruoyi-backend 管理的 agent_chat_message 表。"""

    __tablename__ = "agent_chat_message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=False),
        nullable=False,
        index=True,
    )
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=_now,
        onupdate=_now,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
    )

class Product(Base, TimestampMixin):
    """
    产品模型
    """

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="产品ID")
    name: Mapped[str] = mapped_column(String(30), nullable=False, comment="产品名称")
    description: Mapped[str] = mapped_column(String(255), nullable=False, comment="产品描述")
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="产品价格")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=_now, onupdate=_now)