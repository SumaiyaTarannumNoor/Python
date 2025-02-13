from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models import User
from database import SessionLocal, engine
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000",
    "http://yourfrontenddomain.com", ## just an exaple
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "MI AMOR"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class UserCreate(BaseModel):
    username: str
    password: str

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def  create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username = user.name, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    return "Complete"

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(et_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already snatched!!! Select somethin else.")
    return create_user(db-db, user=user)


def authenticate_user(username: str, password:str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

@app.post("/token")
def login_for_access_token(form_data: OAuthPasswordRequestForm = Depends(), db:Session= Depends(get_db)):
    user = autenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers={"www-authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expires)

