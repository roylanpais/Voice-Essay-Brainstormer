import io
import logging
from typing import Optional
from gtts import gTTS
import config

logger = logging.getLogger(__name__)

def text_to_speech(text: str) -> Optional[bytes]:
    """
    Converts text to speech using gTTS.
    Returns the audio data as bytes.
    """
    try:
        if not text:
            logger.warning("text_to_speech called with empty text.")
            return None
            
        tts = gTTS(text=text, lang=config.TTS_LANG)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception as e:
        logger.error(f"Error in text_to_speech: {e}")
        return None
