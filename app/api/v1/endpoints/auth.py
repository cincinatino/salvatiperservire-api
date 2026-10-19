from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app import models, schemas
from app.api import deps
from app.core import security

router = APIRouter()

# Schema Pydantic per il Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Registrazione pubblica (Fase 1): crea un nuovo account socio con i dati minimi 
    e restituisce un token JWT per l'accesso immediato all'area riservata.
    """
    # 1. Verifica se l'email è già registrata
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utente con questa email risulta già registrato."
        )
    
    # 2. Crea il nuovo utente con password hashata e profilo incompleto
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        nome=user_in.nome,
        cognome=user_in.cognome,
        chiesa=user_in.chiesa,
        citta=user_in.citta,
        profilo_completato=False,  # Indicatore per la Fase 2
        role="socio",
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 3. Genera il token JWT per loggare subito l'utente
    access_token = security.create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o password non corretti"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utente non attivo"
        )
    
    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    """
    Restituisce le informazioni dell'utente attualmente autenticato tramite JWT
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nome": current_user.nome,
        "cognome": current_user.cognome,
        "citta": current_user.citta,
        "chiesa": current_user.chiesa,
        "profilo_completato": current_user.profilo_completato,
        "is_active": current_user.is_active,
        "role": current_user.role
    }