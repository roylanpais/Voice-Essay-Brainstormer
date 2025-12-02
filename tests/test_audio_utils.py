import pytest
from unittest.mock import MagicMock, patch
from audio_utils import text_to_speech

@patch('audio_utils.gTTS')
def test_text_to_speech_success(mock_gTTS):
    mock_tts_instance = MagicMock()
    mock_gTTS.return_value = mock_tts_instance
    
    # Mock write_to_fp to write some bytes
    def side_effect(fp):
        fp.write(b"audio data")
    mock_tts_instance.write_to_fp.side_effect = side_effect
    
    result = text_to_speech("Hello")
    
    assert result == b"audio data"
    mock_gTTS.assert_called_with(text="Hello", lang='en')

def test_text_to_speech_empty():
    result = text_to_speech("")
    assert result is None

@patch('audio_utils.gTTS')
def test_text_to_speech_error(mock_gTTS):
    mock_gTTS.side_effect = Exception("TTS Error")
    
    result = text_to_speech("Hello")
    
    assert result is None
