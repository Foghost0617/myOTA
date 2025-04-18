from passlib.context import CryptContext
from sphinx.ext.todo import TodoList
from sqlalchemy.orm import Session
from backend.models.user import User,Guide,Tourist,GovAdmin,TravelAgency
from backend.schemas.user import UserRegister, UserLogin, UserOut,UserLoginOut
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

    def verify_role(self, input_role: int, db_role: int) -> bool:
        return input_role == db_role

    def register_user(self, user_register: UserRegister) -> UserOut:
        # 检查账号是否已存在
        db_user = self.db.query(User).filter(User.account == user_register.account).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号已存在，请换一个账号注册")

        # 创建新用户，密码加密
        hashed_password = self.hash_password(user_register.password)
        db_user = User(account=user_register.account,
                       password=hashed_password,
                       role=user_register.role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # 根据角色创建子表数据
        try:
            if user_register.role == 1:  # 游客
                tourist = Tourist(user_id=db_user.id)
                self.db.add(tourist)

            elif user_register.role == 2:  # 导游
                guide = Guide(user_id=db_user.id)
                self.db.add(guide)

            elif user_register.role == 3:  # 旅社
                agency = TravelAgency(user_id=db_user.id)
                self.db.add(agency)

            elif user_register.role == 4:  # 文旅局
                gov_admin = GovAdmin(user_id=db_user.id)
                self.db.add(gov_admin)

            else:
                raise HTTPException(status_code=400, detail="无效的用户角色")

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"注册失败：{str(e)}")

        print("注册成功")
        return UserOut.from_orm(db_user)


    def login_user(self, user_login: UserLogin) -> UserLoginOut:
        db_user = self.db.query(User).filter(User.account == user_login.account).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号不存在")

        if not self.verify_password(user_login.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="账号或密码不正确")

        if not self.verify_role(user_login.role, db_user.role):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="身份不匹配")

        print("登录成功")

        response_data = {
            "id": db_user.id,
            "account": db_user.account,
            "role": db_user.role,
        }

        if db_user.role == 3:
            agency = self.db.query(TravelAgency).filter_by(user_id=db_user.id).first()
            if agency:
                response_data["agency_id"] = agency.id
        elif db_user.role == 2:
            guide = self.db.query(Guide).filter_by(user_id=db_user.id).first()
            if guide:
                response_data["guide_id"] = guide.id
        elif db_user.role == 1:
            tourist = self.db.query(Tourist).filter_by(user_id=db_user.id).first()
            if tourist:
                response_data["tourist_id"] = tourist.id
        elif db_user.role == 4:
            gov = self.db.query(GovAdmin).filter_by(user_id=db_user.id).first()
            if gov:
                response_data["gov_id"] = gov.id

        return UserLoginOut(**response_data)