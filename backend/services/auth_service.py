from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserRegister, UserLogin, UserOut
from fastapi import HTTPException, status

# 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    # 密码加密
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    # 验证密码
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, user_register: UserRegister) -> UserOut:
        # 检查账号是否已存在
        db_user = self.db.query(User).filter(User.account == user_register.account).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号已存在，请换一个账号注册")

        # 创建新用户，密码加密
        hashed_password = self.hash_password(user_register.password)
        db_user = User(account=user_register.account, password=hashed_password, role=user_register.role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        print("注册成功")
        return UserOut.from_orm(db_user)

    def login_user(self, user_login: UserLogin) -> UserOut:
        # 检查账号是否存在
        db_user = self.db.query(User).filter(User.account == user_login.account).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="账号不存在")

        # 验证密码
        if not self.verify_password(user_login.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="账号或密码不正确")

        print("登录成功")

        return UserOut.from_orm(db_user)

