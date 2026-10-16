docker exec -it salvatiperservire-api-web-1 python -c "
from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

db = SessionLocal()
email_test = 'admin@salvatiperservire.it'
existing = db.query(User).filter(User.email == email_test).first()
if not existing:
    new_user = User(
        email=email_test,
        hashed_password=get_password_hash('password123'),
        is_active=True,
        role='admin'
    )
    db.add(new_user)
    db.commit()
    print('Utente di test creato con successo!')
else:
    print('Utente di test già esistente.')
db.close()
"