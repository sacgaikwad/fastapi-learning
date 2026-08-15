from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'app.db'}"

print("DATABASE:", DATA_DIR / "app.db")

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)