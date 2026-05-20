import os
import time
from faster_whisper import WhisperModel

def transcribir_audio(wav_path, modelo="medium", device="cpu", compute_type="float32", progress_callback=None):
    if not os.path.exists(wav_path):
        print(f"✖ Archivo de audio no encontrado: {wav_path}")
        return None

    print(f"\n📝 Iniciando transcripción (modelo: {modelo}, precisión: {compute_type})...")
    model = WhisperModel(modelo, device=device, compute_type=compute_type)

    segments, info = model.transcribe(wav_path, beam_size=5, language="en")
    
    # Primera línea con 0 segmentos
    print(f"Transcribiendo audio: 0 segmentos [00:00, ? segmentos/s]   Idioma detectado: {info.language} (probabilidad: {info.language_probability:.2f})")

    base = os.path.splitext(wav_path)[0]
    srt_path = base + "_en.srt"

    start_time = time.time()
    idx = 0
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue
            
            idx += 1
            start = segment.start
            end = segment.end
            
            def to_hmsm(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t % 1) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            f.write(f"{idx}\n{to_hmsm(start)} --> {to_hmsm(end)}\n{text}\n\n")
            
            # Calcular tiempo transcurrido
            elapsed = time.time() - start_time
            minutos = int(elapsed // 60)
            segundos = int(elapsed % 60)
            seg_por_segmento = elapsed / idx if idx > 0 else 0
            
            # Sobrescribir la misma línea en consola
            print(f"\rTranscribiendo audio: {idx} segmentos [{minutos:02d}:{segundos:02d}, {seg_por_segmento:.2f}s/segmento]", end="")
            
            # Enviar a la GUI
            if progress_callback:
                progress_callback(idx, None, f"Transcribiendo audio: {idx} segmentos [{minutos:02d}:{segundos:02d}, {seg_por_segmento:.2f}s/segmento]")
    
    total = idx
    print()  # línea nueva al final
    print(f"✔ Subtítulos en inglés generados: {srt_path} ({total} segmentos)")
    
    if progress_callback:
        progress_callback(total, total)
    
    return srt_path