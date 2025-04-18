
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.user import (UserRegister, UserLogin, UserOut,UserLoginOut)
from backend.services.auth_service import AuthService
from backend.core.database import SessionLocal

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/users",  # 路径前缀
    tags=["用户"]
)

# 注册接口
@router.post("/register", response_model=UserOut)
def register(user_register: UserRegister, db: Session = Depends(get_db)):
    print(user_register)
    auth_service = AuthService(db)
    user=auth_service.register_user(user_register)
    return user



# # 登录接口
# @router.post("/login", response_model=UserOut)
# def login(user_login: UserLogin, db: Session = Depends(get_db)):
#     print(user_login)
#     auth_service = AuthService(db)
#     user = auth_service.login_user(user_login)
#     return user

@router.post("/login", response_model=UserLoginOut)
def login(user_login: UserLogin, db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    user=auth_service.login_user(user_login)
    return user