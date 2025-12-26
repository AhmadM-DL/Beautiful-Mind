# test stt
import pytest
import base64
from src.stt import stt_service

def test_online_stt():
    with open("./tests/test_audio.mp3", "rb") as f:
        base64_audio = base64.b64encode(f.read()).decode("utf-8")
        assert stt_service.transcribe(base64_audio) == "السلام عليكم"