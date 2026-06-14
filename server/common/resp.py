from typing import Any, Generic, TypeVar
from pydantic import BaseModel

# 泛型，让data支持任意模型
T = TypeVar("T")

# 统一返回格式基类
class BaseResp(Generic[T], BaseModel):
    code: int
    message: str
    data: T | None = None

    # 快捷构造静态方法
    @classmethod
    def success(cls, data: Any = None, msg: str = "操作成功") -> "BaseResp":
        return cls(code=200, message=msg, data=data)

    @classmethod
    def fail(cls, code: int = 400, msg: str = "操作失败", data: Any = None) -> "BaseResp":
        return cls(code=code, message=msg, data=data)