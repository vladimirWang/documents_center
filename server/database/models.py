from sqlalchemy import Boolean, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import Base, TimestampMixin


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
    filetype: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件类型")
    vectorized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false(), comment="是否已向量化")