from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import SocioModel
from .schemas import SocioCreate
from .email import invia_email_benvenuto, invia_notifica_admin
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Monta la cartella static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
# Crea le tabelle nel database all'avvio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salvati Per Servire - WebApp", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "API Backend di Salvati Per Servire ODV Onlus attiva e funzionante!"}

@app.post("/api/soci/", status_code=201)
def registra_socio(socio: SocioCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Verifica se il codice fiscale esiste già
    esistente = db.query(SocioModel).filter(SocioModel.codice_fiscale == socio.codice_fiscale).first()
    if esistente:
        raise HTTPException(status_code=400, detail="Un socio con questo Codice Fiscale è già registrato.")
    
    # 2. Inserimento nel database
    nuovo_socio = SocioModel(**socio.model_dump())
    db.add(nuovo_socio)
    db.commit()
    db.refresh(nuovo_socio)
    
    # 3. Accodamento dell'invio email in background
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
