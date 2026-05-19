import subprocess
import os
import shutil
from src.utils import FFMPEG_PATH, DEBUG

def agregar_metadatos_subtitulos(archivo):
    """
    Añade idioma (spa, eng) y disposición 'default' a los subtítulos
    de un archivo MKV/MP4 ya multiplexado.
    Retorna True si tuvo éxito, False en caso contrario.
    """
    if not os.path.exists(archivo):
        print("✖ Archivo no encontrado para agregar metadatos.")
        return False

    temp_file = archivo + ".tmp"
    cmd = [
        FFMPEG_PATH, '-y',
        '-i', archivo.replace('\\', '/'),
        '-c', 'copy',
        '-metadata:s:s:0', 'language=spa', '-metadata:s:s:0', 'title=Español Latino',
        '-metadata:s:s:1', 'language=eng', '-metadata:s:s:1', 'title=English',
        '-disposition:s:s:0', 'default', '-disposition:s:s:1', '0',
        temp_file.replace('\\', '/')
    ]

    if DEBUG:
        print("[DEBUG] Comando metadatos:", ' '.join(cmd))

    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if resultado.returncode == 0:
            shutil.move(temp_file, archivo)
            print("✔ Metadatos de idioma añadidos a los subtítulos.")
            return True
        else:
            if DEBUG:
                print("[DEBUG] Error metadatos:", resultado.stderr[-500:])
            print("⚠ No se pudieron añadir los metadatos. El archivo es funcional sin ellos.")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
    except Exception as e:
        print(f"✖ Excepción agregando metadatos: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False
