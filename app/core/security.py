from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

# Configurazione Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chiave segreta e algoritmo (da spostare nelle variabili d'ambiente / .env)
SECRET_KEY = "CAMBIA_QUESTA_CHIAVE_SEGRETA_IN_PRODUZIONE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 ore

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt