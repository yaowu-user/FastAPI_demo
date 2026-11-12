from typing import Any
from pydantic import BaseModel




class Response(BaseModel):
    """API层统一返回的数据对象"""
      

    code: int 
    msg: str 
    data: Any = None


    @classmethod
    def success(cls, data: Any = None, message: str = "请求成功"):
        # {"code": 200, message: "请求成功", data = None}
        return cls(code=200, msg=message, data=data) 
    @classmethod
    def error(cls, code: int, message: str, data: Any = None):
        # {"code": 500, message: "商品的名称唯一", data = None}
        return cls(code=code, msg=message, data=data)
