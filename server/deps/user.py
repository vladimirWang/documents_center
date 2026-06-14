from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User
from database.session import get_db
from module_user.user_vo import UserRegister


def get_user_by_email(
    email: str,
    db: Session,
):
    # 查询该邮箱用户
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)  # 有数据返回实例，无返回 None


# 校验邮箱是否唯一
def ensure_email_unique(
    user: UserRegister,
    db: Session = Depends(get_db),
) -> None:
    existing_user = get_user_by_email(user.email, db)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="邮箱已存在")
