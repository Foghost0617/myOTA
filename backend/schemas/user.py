from pydantic import BaseModel

# 请求体：注册时用到的字段
class UserRegister(BaseModel):
    account: str
    password: str
    role: int

    class Config:
        from_attributes = True  # 允许将 Pydantic 模型转换为 ORM 模型

#注册/登录返回的字段
class UserOut(BaseModel):
    id: int
    account: str
    role: int

    class Config:
        from_attributes = True

# 请求体：登录时用到的字段
class UserLogin(BaseModel):
    account: str
    password: str
    role: int
