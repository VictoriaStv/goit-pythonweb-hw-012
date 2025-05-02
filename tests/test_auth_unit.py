from src.services.auth import get_password_hash, verify_password, create_access_token
from src.conf.config import settings
from jose import jwt

def test_password_hashing():
    password = "secure123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded
