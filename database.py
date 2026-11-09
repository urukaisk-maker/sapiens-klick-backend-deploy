import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

_raw = os.getenv("DATABASE_URL", "").strip()

if not _raw:
    # Fallback solo para desarrollo local (no funciona en producción)
    _raw = "postgresql://sapiens:sapiens_pass@db:5432/sapiens_klick"
    print("[WARNING] DATABASE_URL no configurada. Usando fallback local.")

if not _raw.startswith(("postgresql://", "postgresql+psycopg2://")):
    raise RuntimeError(
        f"DATABASE_URL inválida. Debe empezar por 'postgresql://'. "
        f"Valor recibido (censurado): '{_raw[:20]}...'"
    )

DATABASE_URL = _raw.replace("postgresql://", "postgresql+psycopg2://")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()