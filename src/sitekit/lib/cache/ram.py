CACHE = {}
memoria_occupata = 0
memoria_massima = 4194304  # 4Mb al massimo

def carica(chiave: str) -> dict | None:
    return CACHE.get(chiave)

def salva(chiave: str, valore: object) -> bool:
    global memoria_occupata
    global memoria_massima

    if (memoria_occupata + len(valore)) < memoria_massima:
        CACHE[chiave] = valore
        memoria_occupata += len(valore)
        return True
    else:
        return False
from typing import Any
import pickle

CACHE: dict[str, Any] = {}
memoria_occupata = 0  # byte stimati (basati su pickle)
memoria_massima = 4 * 1024 * 1024  # 4 MB

def _peso(valore: Any) -> int:
    """Stima del peso in RAM usando la dimensione del pickle serializzato."""
    try:
        return len(pickle.dumps(valore, protocol=pickle.HIGHEST_PROTOCOL))
    except Exception:
        return 0

def carica(chiave: str) -> Any | None:
    return CACHE.get(chiave)

def salva(chiave: str, valore: Any) -> bool:
    global memoria_occupata, memoria_massima
    nuovo = _peso(valore)
    # Se già presente, rimuovi il vecchio peso dal contatore
    if chiave in CACHE:
        memoria_occupata -= _peso(CACHE[chiave])
    if (memoria_occupata + nuovo) <= memoria_massima:
        CACHE[chiave] = valore
        memoria_occupata += nuovo
        return True
    else:
        # ripristina il contatore se avevi sottratto il vecchio
        if chiave in CACHE:
            memoria_occupata += _peso(CACHE[chiave])
        return False