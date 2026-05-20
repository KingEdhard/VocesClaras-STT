import os
import time
from faster_whisper import WhisperModel

def transcribir_audio(wav_path, modelo="medium", device="cpu", compute_type="float32", progress_callback=None):
    """
    Transcribe el WAV a inglés con faster-whisper.
    Muestra progreso en consola con tiempo real.
    Envía el mismo mensaje a la GUI mediante callback.
    """
    if not os.path.exists(wav_path):
        print(f"✖ Archivo de audio no encontrado: {wav_path}")
        return None

    print(f"\n📝 Iniciando transcripción (modelo: {modelo}, precisión: {compute_type})...")
    model = WhisperModel(modelo, device=device, compute_type=compute_type)

    segments, info = model.transcribe(wav_path, beam_size=5, language="en")
    print(f"   Idioma detectado: {info.language} (probabilidad: {info.language_probability:.2f})")

    base = os.path.splitext(wav_path)[0]
    srt_path = base + "_en.srt"

    # Recolectar segmentos para saber el total
    segmentos_lista = []
    for segment in segments:
        if segment.text.strip():
            segmentos_lista.append(segment)
    
    total = len(segmentos_lista)
    start_time = time.time()
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segmentos_lista, 1):
            start = segment.start
            end = segment.end
            text = segment.text.strip()
            
            def to_hmsm(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t % 1) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            f.write(f"{idx}\n{to_hmsm(start)} --> {to_hmsm(end)}\n{text}\n\n")
            
            # Calcular estadísticas
            elapsed = time.time() - start_time
            minutos = int(elapsed // 60)
            segundos = int(elapsed % 60)
            seg_por_segmento = elapsed / idx if idx > 0 else 0
            
            # Mostrar en consola (como lo hacía tqdm)
            print(f"\rTranscribiendo audio: {idx} segmentos [{minutos:02d}:{segundos:02d}, {seg_por_segmento:.2f}s/segmento]", end="")
            
            # Enviar a la GUI el mismo mensaje
            if progress_callback:
                mensaje_gui = f"Transcribiendo audio: {idx} segmentos [{minutos:02d}:{segundos:02d}, {seg_por_segmento:.2f}s/segmento]"
                progress_callback(idx, total, mensaje_gui)
    
    print()  # línea nueva al final
    print(f"✔ Subtítulos en inglés generados: {srt_path} ({total} segmentos)")
    return srt_path