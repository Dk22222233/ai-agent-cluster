from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker,declarative_base
DB_URL="postgresql+psycopg://fastapi:mysecretpassword@localhost:5432/fastapi_db"
engine =create_engine(DB_URL)
session=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
Base=declarative_base()

