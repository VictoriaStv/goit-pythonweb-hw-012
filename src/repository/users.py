from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas.auth import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def create_user(user_data: UserCreate, db: Session) -> User:
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
