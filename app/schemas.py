from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

# Schema per la Pre-Registrazione (Fase 1)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nome: str
    cognome: str
    chiesa: Optional[str] = None
    citta: Optional[str] = None

# Schema per il completamento del profilo nell'Area Riservata (Fase 2)
class UserProfileUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    codice_fiscale: Optional[str] = None
    telefono: Optional[str] = None
    citta: Optional[str] = None
    chiesa: Optional[str] = None

# Schema di risposta per i dati dell'utente
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nome: Optional[str] = None
    cognome: Optional[str] = None
    citta: Optional[str] = None
    chiesa: Optional[str] = None
    profilo_completato: bool
    role: str

    class Config:
        from_attributes = True
    
class SocioCreate(BaseModel):
    cognome: str
    nome: str
    data_nascita: date
    luogo_nascita: str
    codice_fiscale: str = Field(..., min_length=16, max_length=16)
    indirizzo: str
    cap: str = Field(..., min_length=5, max_length=5)
    citta: str
    provincia: str = Field(..., min_length=2, max_length=2)
    telefono: Optional[str] = None
    cellulare: str
    email: EmailStr
    titolo_studio: Optional[str] = None
    gruppo_sanguigno_tipo: Optional[str] = None
    gruppo_sanguigno_rh: Optional[str] = None
    esperienze_brevetti: Optional[str] = None
    chiesa_appartenenza: str
    chiesa_citta: str
    anziano_responsabile_nome: Optional[str] = None
    accetta_statuto: bool
    consenso_dati_personali: bool
    consenso_newsletter: Optional[bool] = False

    class Config:
        from_attributes = True
