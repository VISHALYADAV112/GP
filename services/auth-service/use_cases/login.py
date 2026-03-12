"""
Login use case
"""
import sys
import os
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../db-schemas'))
from models import User
from repositories.user_repository import UserRepository


class LoginUseCase:
    """Handle user login logic"""
    
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo or UserRepository()
    
    def execute(self, db: Session, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Execute login
        
        Returns:
            (success, user, message)
        """
        # Get user by username
        user = self.user_repo.get_by_username(db, username)
        
        if not user:
            return False, None, "Invalid username or password"
        
        # Verify password
        if not user.verify_password(password):
            return False, None, "Invalid username or password"
        
        # Check if account is active
        if user.status != "active":
            return False, None, f"Account is {user.status}"
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return True, user, "Login successful"
