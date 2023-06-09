import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def create_secret_key(length: int) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_secret_key(db: Session) -> str:
    key = create_secret_key(5)
    while crud.get_db_url_by_key(db, key):
        key = create_secret_key()
    return key


