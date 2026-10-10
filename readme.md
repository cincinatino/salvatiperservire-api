# 🤝 Salvati Per Servire ODV Onlus - Web Registration System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An automated member registration system developed for the **Salvati per Servire ODV Onlus** association. Designed for high reliability, low maintenance overhead, easy deployment via Docker, and full compliance with GDPR (EU 2016/679) regulations regarding sensitive personal data processing.

---

## 📌 Project Overview

This system streamlines the onboarding process for new members (*soci*) of the ONLUS. It collects registration details (personal information, emergency contacts, religious affiliation, health/blood type data where required), persists them securely in PostgreSQL, and triggers automated email workflows.

### Key Objectives
* **GDPR Compliance**: Strict adherence to Italian and EU privacy standards for sensitive data processing.
* **Low Overhead & Stability**: Lightweight Python/FastAPI backend chosen over heavy Node.js setups to ensure minimal dependency auditing and long-term stability.
* **Automation**: Immediate background notifications to both newly registered members and administrators.
* **Self-Hosted Readiness**: Easily deployed on lightweight hardware (e.g., Raspberry Pi) using Docker Compose.

---

## 🏗 System Architecture & Stack

```
   +-------------------------------------------------------------+
   |                       Client / Browser                      |
   +-------------------------------------------------------------+
                                  |
                                  v
   +-------------------------------------------------------------+
   |                        Docker Host                          |
   |                                                             |
   |   +---------------------+         +---------------------+   |
   |   |   FastAPI Service   | <-----> |     PostgreSQL      |   |
   |   |    (Uvicorn API)    |         |     Database        |   |
   |   +---------------------+         +---------------------+   |
   |              |                                              |
   |              v                                              |
   |     Background Tasks                                        |
   |     (Email Workflow)                                        |
   +-------------------------------------------------------------+
```

* **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
* **Database**: [PostgreSQL 15](https://www.postgresql.org/)
* **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) & [Pydantic v2](https://docs.pydantic.dev/)
* **Containerization**: [Docker](https://www.docker.com/) & Docker Compose
* **Asynchronous Jobs**: FastAPI `BackgroundTasks` for transaction email dispatching

---

## 🚀 Current Status

- [x] Docker & Docker Compose setup with multi-container configuration (API + DB).
- [x] Database schema (`SocioModel`) defined and initialized with SQLAlchemy.
- [x] RESTful API endpoint (`POST /api/soci/`) fully operational with duplicate code checks (`Codice Fiscale`).
- [x] Interactive OpenAPI / Swagger UI accessible (`/docs`).
- [x] Non-blocking email dispatch system implemented (supports simulation mode & SMTP integration).
- [x] Git repository initialized and pushed via SSH to GitHub.
- [ ] Frontend user interface for form submission.
- [ ] Social OAuth authentication (Google / Apple Login).
- [ ] Production SMTP credential provisioning.

---

## 📜 Project Changelog & History

### Step 1: Foundation & Containerization
* Settled on Python/FastAPI + PostgreSQL tech stack for system stability and low maintenance.
* Configured `docker-compose.yml` to orchestrate web and database services seamlessly.

### Step 2: Database Schema & API Setup
* Created `SocioModel` matching official "Foglio iscrizione" requirements.
* Built primary endpoint `POST /api/soci/` to record new memberships safely into PostgreSQL.

### Step 3: Transactional Notification System
* Built `app/email.py` using FastAPI's `BackgroundTasks` to send non-blocking welcome emails to members and enrollment alerts to administrators.
* Integrated simulation mode for logging email bodies directly to Docker stdout prior to SMTP credential configuration.

### Step 4: Version Control & GitHub Integration
* Configured local Git repository with tailored `.gitignore`.
* Linked local environment to GitHub via SSH (`git@github.com:cincinatino/salvatiperservire-api.git`).

---

## ⚙️ Local Development & Quickstart

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/) installed on host system.

### 1. Clone the repository
```bash
git clone git@github.com:cincinatino/salvatiperservire-api.git
cd salvatiperservire-api
```

### 2. Launch with Docker Compose
```bash
docker compose up --build -d
```

### 3. Verify status & logs
```bash
docker compose logs -f web
```

### 4. Access the API
* **Base URL**: `http://localhost:8000`
* **Swagger Documentation**: `http://localhost:8000/docs`
* **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## ✉️ Email Configuration (Environment Variables)

To activate live SMTP dispatching, update the `environment` section in `docker-compose.yml`:

```yaml
environment:
  - DATABASE_URL=postgresql://admin:secretpassword@db:5432/salvatiperservire
  - SMTP_SERVER=smtp.yourprovider.com
  - SMTP_PORT=587
  - SMTP_USER=your-email@yourdomain.com
  - SMTP_PASSWORD=your-secret-password
  - ADMIN_EMAIL=info@salvatiperservire.it
```

*Note: Leaving `SMTP_USER` and `SMTP_PASSWORD` empty defaults the system to local console simulation mode.*

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).