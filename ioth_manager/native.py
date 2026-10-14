import ctypes
import os
from pathlib import Path

# Percorso della libreria compilata

'''
LIB_PATH = Path(__file__).resolve().parent.parent / "c_src" / "libioth_bridge.so"

if not LIB_PATH.exists():
    raise FileNotFoundError(f"Libreria nativa non trovata in {LIB_PATH}. Compila prima con 'make' in c_src/")

# Caricamento del binario
_lib = ctypes.CDLL(str(LIB_PATH))

# Configurazione tipi di input/output per sicurezza dei tipi (argtypes e restype)
_lib.ioth_bridge_init.argtypes = [ctypes.c_char_p]
_lib.ioth_bridge_init.restype = ctypes.c_int

_lib.ioth_bridge_version.argtypes = []
_lib.ioth_bridge_version.restype = ctypes.c_char_p

def get_bridge_version() -> str:
"""Restituisce la versione del modulo C."""
    res = _lib.ioth_bridge_version()
    return res.decode("utf-8")

def init_stack(stack_name: str) -> bool:
    """Inizializza uno stack IoTh chiamando la funzione C."""
    c_str = stack_name.encode("utf-8")
    status = _lib.ioth_bridge_init(c_str)
    return status == 0

'''
def init_stack(stack_name: str) -> bool:
    return True

def get_bridge_version() -> str:
    """Restituisce la versione del modulo C."""
    return "test"