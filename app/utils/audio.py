import base64
import io

def encode_audio_base64(audio_bytes: bytes) -> str:
    """Encodes audio bytes to a base64 string."""
    return base64.b64encode(audio_bytes).decode('utf-8')

def decode_audio_base64(base64_string: str) -> bytes:
    """Decodes a base64 string to audio bytes."""
    return base64.b64decode(base64_string)

def get_content_type(format: str) -> str:
    """Returns the MIME type for a given audio format."""
    format = format.lower()
    if format == 'wav':
        return 'audio/wav'
    elif format == 'mp3':
        return 'audio/mpeg'
    elif format == 'pcm':
        return 'audio/pcm' # Note: PCM usually needs container like WAV
    else:
        return 'application/octet-stream'
