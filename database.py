import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def _clean_url(raw: str) -> str:
    """Limpia caracteres que se cuelan al copiar/pegar (backticks, comillas, espacios, BOM)."""
    if not raw:
        return ""
    s = raw.strip()
    # BOM y caracteres invisibles
    s = (s
         .replace("\ufeff", "")
         .replace("\u200b", "")
         .replace("\u200c", "")
         .replace("\u200d", "")
         .replace("\u00a0", " "))
    # Backticks, comillas y otros caracteres que se pegan al copiar
    s = re.sub(r"^[`'\"´ʻʽʾʿˮ„«»\s]+", "", s)
    s = re.sub(r"[`'\"´ʻʽʾʿˮ„«»\s]+$", "", s)
    return s.strip()


_raw = _clean_url(os.getenv("DATABASE_URL", ""))

if not _raw:
    _raw = "postgresql://sapiens:sapiens_pass@db:5432/sapiens_klick"
    print("[WARNING] DATABASE_URL no configurada. Usando fallback local.")

if not _raw.startswith(("postgresql://", "postgresql+psycopg2://")):
    raise RuntimeError(
        f"DATABASE_URL inválida incluso tras limpieza. "
        f"Valor recibido (censurado): '{_raw[:30]}...'"
    )

DATABASE_URL = _raw.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()