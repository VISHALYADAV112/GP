"""Custom exceptions for Gram Panchayat system"""


class GPBaseException(Exception):
    """Base exception for GP system"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(GPBaseException):
    """Validation error"""
    pass


class NotFoundError(GPBaseException):
    """Resource not found"""
    pass


class AuthenticationError(GPBaseException):
    """Authentication failed"""
    pass


class AuthorizationError(GPBaseException):
    """Insufficient permissions"""
    pass


class DuplicateError(GPBaseException):
    """Duplicate resource"""
    pass


class BusinessLogicError(GPBaseException):
    """Business logic violation"""
    pass


class DatabaseError(GPBaseException):
    """Database operation error"""
    pass
