import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurazioni lette dalle variabili d'ambiente (Docker Compose)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "info@salvatiperservire.it") # Preso dai contatti ufficiali[cite: 1]

def _invia_email(destinatario: str, oggetto: str, corpo_html: str):
    """Funzione interna per l'invio effettivo tramite SMTP o simulazione in console."""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"\n--- [SIMULAZIONE INVIO EMAIL] ---")
        print(f"A: {destinatario}")
        print(f"Oggetto: {oggetto}")
        print(f"Contenuto:\n{corpo_html}")
        print(f"-----------------------------------\n")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = destinatario
        msg["Subject"] = oggetto
        
        msg.attach(MIMEText(corpo_html, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, destinatario, msg.as_string())
        print(f"Email inviata con successo a {destinatario}")
    except Exception as e:
        print(f"Errore durante l'invio dell'email a {destinatario}: {e}")

def invia_ email_benvenuto(socio_email: str, socio_nome: str, socio_cognome: str):
    """Invia l'email di benvenuto al nuovo socio."""
    oggetto = "Benvenuto in Salvati Per Servire ODV Onlus"
    corpo = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <h2>Benvenuto/a caro {socio_cognome} {socio_nome},</h2>
        <p>La tua richiesta di iscrizione all'associazione <b>Salvati Per Servire ODV </b> è stata registrata con successo nel nostro sistema.</p>
        <p>Ti ricordiamo che la quota associativa annua è di <b>€36,00</b> e va versata secondo le modalità indicate nello statuto dell'associazione[cite: 1].</p>
        <p>Grazie per esserti unito/a alla nostra comunità!</p>
        <br>
        <p>Cordiali saluti,</p>
        <p><b>Salvati Per Servire ODV Onlus</b></p>
    </div>
    """
    _invia_email(socio_email, oggetto, corpo)

def invia_notifica_admin(socio_email: str, socio_nome: str, socio_cognome: str, codice_fiscale: str):
    """Invia una notifica all'amministratore / presidente della ONLUS."""
    oggetto = f"[WebApp] Nuova iscrizione socio: {socio_cognome} {socio_nome}"
    corpo = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <h2>Nuova Registrazione Socio</h2>
        <p>Un nuovo utente ha completato il modulo di iscrizione online:</p>
        <ul>
            <li><b>Nominativo:</b> {socio_cognome} {socio_nome}</li>
            <li><b>Codice Fiscale:</b> {codice_fiscale}</li>
            <li><b>E-mail:</b> {socio_email}</li>
        </ul>
        <p>Accedi al database o al pannello di amministrazione per verificare i dati completi.</p>
    </div>
    """
    _invia_email(ADMIN_EMAIL, oggetto, corpo)
