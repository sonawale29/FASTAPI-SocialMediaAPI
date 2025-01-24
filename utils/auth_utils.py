from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt

# Create an instance of CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = "sUpN8WeRmHuUvSc30A8xlLZM-IhWOqfV-Qv4x-U6UZA"  # Change this to a secure value
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes


def hash_password(password: str) -> str:
    """
    Hash the password using bcrypt hashing algorithm.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the given plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Function to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify JWT token
def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def extract_token_from_header(authorization: str) -> str:
    """
    Extract the token from the Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    return authorization.split("Bearer ")[1]

