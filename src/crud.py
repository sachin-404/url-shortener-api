from sqlalchemy.orm import Session
from configs import models, schemas
from . import keygen

def create_db_url(url: schemas.URLBase, db: Session) -> models.URL:
    key = keygen.create_unique_secret_key(db)
    secret_key = f"{key}_{keygen.create_secret_key(8)}"
    
    db_url = models.URL(
        input_url=url.input_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db:Session, key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.key == key, models.URL.is_active).first()
    
def get_db_url_by_secret_key(db:Session, secret_key: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.secret_key == secret_key, models.URL.is_active).first()

def update_click_count(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
