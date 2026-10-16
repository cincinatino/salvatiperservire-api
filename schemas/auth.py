from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema per il Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Schema per la Risposta con Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Payload memorizzato nel JWT
class TokenPayload(BaseModel):
    sub: Optional[str] = None