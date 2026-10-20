import os
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import SocioModel
from .schemas import SocioCreate
from .email import invia_email_benvenuto, invia_notifica_admin
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.endpoints import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salvati Per Servire - WebApp", version="1.0.0")

os.makedirs("app/static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticazione"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Utenti e Profilo (Fase 2)"])

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/api/soci/", status_code=201)
def registra_socio(socio: SocioCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # erifica se il codice fiscale esiste già
    esistente = db.query(SocioModel).filter(SocioModel.codice_fiscale == socio.codice_fiscale).first()
    if esistente:
        raise HTTPException(status_code=400, detail="Un socio con questo Codice Fiscale è già registrato.")
    
   
    nuovo_socio = SocioModel(**socio.model_dump())
    db.add(nuovo_socio)
    db.commit()
    db.refresh(nuovo_socio)
    
    background_tasks.add_task(
        invia_email_benvenuto, 
        socio_email=nuovo_socio.email, 
        socio_nome=nuovo_socio.nome, 
        socio_cognome=nuovo_socio.cognome
    )
    
    background_tasks.add_task(
        invia_notifica_admin, 
        socio_email=nuovo_socio.email, 
        socio_nome=nuovo_socio.nome, 
        socio_cognome=nuovo_socio.cognome, 
        codice_fiscale=nuovo_socio.codice_fiscale
    )
    
    return {
        "message": "Iscrizione completata con successo! Email di benvenuto in coda.", 
        "id": nuovo_socio.id
    }