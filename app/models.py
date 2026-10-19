# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, DateTime, Text
from datetime import datetime
from .database import Base

class SocioModel(Base):
    __tablename__ = "soci"

    id = Column(Integer, primary_key=True, index=True)
    cognome = Column(String(100), nullable=False)
    nome = Column(String(100), nullable=False)
    data_nascita = Column(Date, nullable=False)
    luogo_nascita = Column(String(100), nullable=False)
    codice_fiscale = Column(String(16), unique=True, index=True, nullable=False)
    
    # Indirizzo e Contatti
    indirizzo = Column(String(200), nullable=False)
    cap = Column(String(5), nullable=False)
    citta = Column(String(100), nullable=False)
    provincia = Column(String(2), nullable=False)
    telefono = Column(String(20), nullable=True)
    cellulare = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, index=False, nullable=False)
    
    # Dati Specifici
    titolo_studio = Column(String(100), nullable=True)
    gruppo_sanguigno_tipo = Column(String(5), nullable=True) # Es. A, B, AB, 0
    gruppo_sanguigno_rh = Column(String(2), nullable=True)   # Es. +, -
    esperienze_brevetti = Column(Text, nullable=True)
    
    # Dati Ecclesiastici
    chiesa_appartenenza = Column(String(150), nullable=False)
    chiesa_citta = Column(String(100), nullable=False)
    anziano_responsabile_nome = Column(String(150), nullable=True)
    
    # Quota e Consensi GDPR
    quota_annua = Column(Numeric(10, 2), default=36.00)
    accetta_statuto = Column(Boolean, default=False)
    consenso_dati_personali = Column(Boolean, default=False)
    consenso_newsletter = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable per consentire futuri Social Login senza password
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="socio")  # "socio", "admin", ecc.
    created_at = Column(DateTime, default=datetime.utcnow)
# Campi Anagrafici & Profilo (Fase 2 / Area Riservata)
    nome = Column(String, nullable=True)
    cognome = Column(String, nullable=True)
    codice_fiscale = Column(String, unique=True, index=True, nullable=True)
    telefono = Column(String, nullable=True)
    citta = Column(String, nullable=True)
    chiesa = Column(String, nullable=True)
    foto_tessera_url = Column(String, nullable=True)
    profilo_completato = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)