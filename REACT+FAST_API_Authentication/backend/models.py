from sqlalchemy import Column, Integer, String
from database import Base
from database import engine

class User(Base):
    __table__="users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


User.metadata.create_all(bind=engine)    