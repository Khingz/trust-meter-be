from sqlalchemy.orm import Session
from app.schemas.user import RegisterUserInput, LoginUserInput, PasswordResetInput
from app.models.user import User
from fastapi import HTTPException
from app.utils.auth import hash_password, verify_password, create_password_token, verify_password_token
from app.utils.settings import settings

class UserService:
    """ User service class """
    def create(self, db: Session, schema: RegisterUserInput):
        """Create a new user account"""
        if db.query(User).filter(User.email == schema.email).first():
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )
        schema.password = hash_password(password=schema.password)
        user = User(**schema.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    def login_user(self, db: Session, schema: LoginUserInput):
        """Login a user"""
        user = db.query(User).filter(User.email == schema.email).first()
        print(user)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password",
            )
        if not verify_password(plain_password=schema.password, hashed_password=user.password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password",
            )
        return user

    def get_user_by_id(self, db: Session, id: str):
        """Get the user by Id"""
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def get_user_by_email(self, db: Session, email: str):
        """Get the user by email"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def password_reset_token(self, db:Session, email: str):
        """"""
        user = self.get_user_by_email(db=db, email=email)
        reset_token = create_password_token(user_email=user.email)
        user.password_reset_token = reset_token
        db.commit()
        db.refresh(user)
        reset_link = settings.CLIENT_URL + f"/reset-password/{reset_token}"
        return {
            "reset_link": reset_link,
            "name": user.name,
            "email": user.email
        }
    
    def reset_password(self, db: Session, schema: PasswordResetInput):
        """"""
        user = verify_password_token(schema.token, db)
        hashed_password = hash_password(password=schema.password)
        user.password = hashed_password
        user.password_reset_token = None
        db.commit()
        db.refresh(user)
        return {
            "name": user.name,
            "email": user.email
        }
    
        

user_service = UserService()
