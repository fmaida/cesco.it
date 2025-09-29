from pathlib import Path

# Risali a partire dal file corrente 
# (__file__) fino a trovare pyproject.toml
def get_base_dir() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Non trovo la root del progetto (pyproject.toml mancante?)")

# --------------------------------------------
# QUESTI PARAMETRI POSSONO ESSERE MODIFICATI
# PER ADATTARLI ALLE NECESSITÀ DEL PROGETTO
#
BASE_URL = "https://www.example.com"  # Cambia con l'URL del tuo sito
#
# --------------------------------------------
BASE_DIR = get_base_dir()
CACHE_DIR = BASE_DIR / ".cache"
BUILD_DIR = BASE_DIR / "build"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
I18N_DIR = BASE_DIR / "i18n"
CONTENT_DIR = BASE_DIR / "content"