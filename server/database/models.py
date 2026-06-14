from database.base_model import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.base_model import TimestampMixin

class User(Base, TimestampMixin):
    """
    用户模型
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(255), nullable=False, comment="用户名")
    email: Mapped[str] = mapped_column(String(255), nullable=False, comment="邮箱")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")