import os

DEBUG = True  # Cambiar a True para depuración

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(ROOT_DIR, 'bin')

FFMPEG_PATH = os.path.join(BIN_DIR, 'ffmpeg.exe')
FFPROBE_PATH = os.path.join(BIN_DIR, 'ffprobe.exe')

if not os.path.isfile(FFMPEG_PATH):
    raise FileNotFoundError(f"No se encontró ffmpeg.exe en {FFMPEG_PATH}")
if not os.path.isfile(FFPROBE_PATH):
    raise FileNotFoundError(f"No se encontró ffprobe.exe en {FFPROBE_PATH}")

def input_validado(prompt, opciones_validas=None, intentos=3, map_alias=None, defecto=None):
    map_alias = map_alias or {}
    opciones = {o.lower() for o in opciones_validas} if opciones_validas else None
    for _ in range(intentos):
        r = input(prompt).strip()
        if r == '' and defecto is not None:
            return defecto
        r_norm = r.lower()
        if r_norm in map_alias:
            r_norm = map_alias[r_norm]
        if opciones is None or r_norm in opciones:
            return r_norm
        print("Entrada no válida. Opciones válidas:", ", ".join(sorted(opciones)))
    return None
