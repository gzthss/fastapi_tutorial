from pydantic import BaseModel

class TokenData(BaseModel):
    """JWT Token payload schema."""
    username: str | None = None

class UserCreate(BaseModel):
    """User registration request schema."""
    username: str
    password: str
    email: str
    
class TokenResponse(BaseModel):
    """Login response schema."""
    access_token: str
    token_type: str
    


