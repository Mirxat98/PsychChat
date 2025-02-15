from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt
from .database import SessionLocal, init_db
from .models import User

app = FastAPI()

# 初始化数据库
init_db()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 用户注册模型
class RegisterUser(BaseModel):
    email: str
    password: str

# 用户注册 API
@app.post("/api/auth/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # 检查用户是否已存在
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户已存在")

    # 哈希密码
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 创建用户
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message": "注册成功"}
