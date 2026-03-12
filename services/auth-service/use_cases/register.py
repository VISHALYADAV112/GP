"""
User registration use case
"""
import sys
import os
from typing import Tuple, Optional
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import User
from repositories.user_repository import UserRepository


class RegisterUseCase:
    """Handle user registration logic"""
    
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo or UserRepository()
    
    def execute(
        self,
        db: Session,
        username: str,
        password: str,
        email: str,
        full_name: str,
        role: str,
        gram_panchayat_id: Optional[int] = None
    ) -> Tuple[bool, Optional[User], str]:
        """
        Execute user registration
        
        Returns:
            (success, user, message)
        """
        # Check if username exists
        existing_user = self.user_repo.get_by_username(db, username)
        if existing_user:
            return False, None, "Username already exists"
        
        # Check if email exists
        if email:
            existing_email = self.user_repo.get_by_email(db, email)
            if existing_email:
                return False, None, "Email already registered"
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            gram_panchayat_id=gram_panchayat_id,
            status="active"
        )
        new_user.set_password(password)
        
        # Save to database
        user = self.user_repo.create(db, new_user)
        
        return True, user, "User registered successfully"
