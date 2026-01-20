import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./app/data.db')

def get_database_url():
    # Get database URL from environment variable .env. Fall back to SQLite if not set.
    env_url = os.getenv('DATABASE_URL')
    
    if not env_url:
        return 'sqlite:///./app/data.db'
    
    if env_url.startswith('sqlite'):
        return env_url

    try:
        test_engine = create_engine(env_url, connect_args={'connect_timeout': 2})
        with test_engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return env_url
    except Exception:
        print(f'Warning: could not connect to Postgres at {env_url}')
        print('Fall back to SQLite db')
        return 'sqlite:///./app/data.db'


DATABASE_URL = get_database_url()

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