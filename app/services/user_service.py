from sqlalchemy.orm import Session
from app.schemas.user import RegisterUserInput, LoginUserInput, PasswordResetInput, PasswordUpdate, UserUpdate
from app.models.user import User
from fastapi import HTTPException
from app.utils.auth import hash_password, verify_password, create_password_token, verify_password_token
from app.utils.settings import settings
from uuid import UUID

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
        """Reset user password """
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
        
    def change_password(self, db: Session, schema: PasswordUpdate, user):
        """Change user password"""
        if schema.old_password == schema.new_password:
            raise HTTPException(
                status_code=400,
                detail="Old pssword and new password cannot be the same",
            )
            
        if not verify_password(plain_password=schema.old_password, hashed_password=user.password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect old password",
            )
            
        hashed_password = hash_password(password=schema.new_password)
        user.password = hashed_password
        user.password_reset_token = None
        db.commit()
        db.refresh(user)
        return {
            "name": user.name,
            "email": user.email
        }
        
    def update_user(self, db: Session, schema: UserUpdate, user):
        """Update User info """
        user = self.get_user_by_id(db=db, id=user.id)
        user.name = schema.name
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_id(self, db: Session, id: UUID):
        """Get user by Id"""
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
        

user_service = UserService()
