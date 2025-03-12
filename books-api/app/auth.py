from datetime import datetime, timedelta
from typing import Optional

# importer secret_key de secret_key.py
from app.secret_key import SECRET_KEY
from jose import jwt

# Normally, the secret key should be kept secret and ideally loaded from an environment variable
# But to simplify, we are hardcoding it here
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT token with the provided data.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
