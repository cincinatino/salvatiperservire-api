import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.put("/me/profile", response_model=schemas.UserResponse)
async def update_user_profile(
    nome: Optional[str] = Form(None),
    cognome: Optional[str] = Form(None),
    codice_fiscale: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    citta: Optional[str] = Form(None),
    chiesa: Optional[str] = Form(None),
    foto_tessera: Optional[UploadFile] = File(None),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Fase 2: L'utente autenticato (Bearer Token) completa i suoi dati anagrafici
    e/o carica la propria foto tessera. Imposta profilo_completato = True.
    """
    # 1. Aggiornamento campi anagrafici base
    if nome is not None:
        current_user.nome = nome
    if cognome is not None:
        current_user.cognome = cognome
    if telefono is not None:
        current_user.telefono = telefono
    if citta is not None:
        current_user.citta = citta
    if chiesa is not None:
        current_user.chiesa = chiesa

    # 2. Controllo duplicati Codice Fiscale
    if codice_fiscale is not None:
        existing_cf = db.query(models.User).filter(
            models.User.codice_fiscale == codice_fiscale,
            models.User.id != current_user.id
        ).first()
        if existing_cf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Questo Codice Fiscale è già stato registrato da un altro utente."
            )
        current_user.codice_fiscale = codice_fiscale

    # 3. Gestione e salvataggio della Foto Tessera
    if foto_tessera:
        upload_dir = "app/static/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Mantiene l'estensione originale (.jpg, .png, ecc.)
        extension = foto_tessera.filename.split(".")[-1] if "." in foto_tessera.filename else "jpg"
        filename = f"user_{current_user.id}_tessera.{extension}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto_tessera.file, buffer)

        current_user.foto_tessera_url = f"/static/uploads/{filename}"

    # 4. Imposta lo stato del profilo come completato
    current_user.profilo_completato = True

    db.commit()
    db.refresh(current_user)

    return current_user