import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DATABASE_URL = 'sqlite:///./app/data.db'

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={'check_same_thread': False},
# )

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./app/data.db')

connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

print("DATABASE_URL =", DATABASE_URL)
print("ENGINE DB   =", str(engine.url))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()