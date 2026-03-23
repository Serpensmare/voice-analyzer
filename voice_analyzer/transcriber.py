"""
Voice transcriber using faster-whisper.
Produces timestamped segments with optional speaker labels.
"""
import os
import datetime
from faster_whisper import WhisperModel

MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")
_model = None

def get_model():
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model

def transcribe(audio_path: str, language: str = None) -> dict:
    """
    Transcribe audio file. Returns dict with:
    - segments: list of {start, end, text, speaker}
    - language: detected language
    - duration: total duration in seconds
    - full_text: complete transcript
    """
    model = get_model()
    lang = None if language in (None, "auto") else language

    segments_raw, info = model.transcribe(
        audio_path,
        language=lang,
        beam_size=5,
        vad_filter=True,
    )

    segments = []
    full_parts = []

    for seg in segments_raw:
        text = seg.text.strip()
        if not text:
            continue
        segments.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": text,
            "speaker": "Speaker"  # diarization not available on Pi ARM
        })
        full_parts.append(text)

    return {
        "segments": segments,
        "language": info.language,
        "duration": round(segments[-1]["end"] if segments else 0, 1),
        "full_text": " ".join(full_parts),
        "audio_file": os.path.basename(audio_path),
        "transcribed_at": datetime.datetime.now().isoformat()
    }
