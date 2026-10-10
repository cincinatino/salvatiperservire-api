FROM python:3.12-slim

WORKDIR /app

# Installa le dipendenze di sistema necessarie per PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copia e installa i requisiti Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente
COPY . .

# Avvia l'applicazione con ricaricamento automatico in sviluppo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
