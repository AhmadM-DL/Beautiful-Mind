import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

@patch("app.stt_service.transcribe")
def test_speech_to_text_success(mock_transcribe):
    mock_transcribe.return_value = "السلام عليكم"

    payload = {
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }

    response = client.post("/api/stt", json=payload)

    assert response.status_code == 200
    assert response.json() == {"transcription": "السلام عليكم"}
    mock_transcribe.assert_called_once_with(payload["base64_audio"])


@patch("app.stt_service.transcribe")
def test_speech_to_text_failure(mock_transcribe):
    mock_transcribe.side_effect = Exception("STT failed")

    payload = {
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }

    response = client.post("/api/stt", json=payload)

    assert response.status_code == 500


# -------------------------
# /api/anonymize
# -------------------------

@patch("app.anonymizer_service.anonymize")
def test_anonymize_success(mock_anonymize):
    mock_anonymize.return_value = "ذهبت بالأمس مع شخص إلى دكان السعداء"

    payload = {
        "text": "ذهبت بالأمس مع ركان إلى دكان السعداء"
    }

    response = client.post("/api/anonymize", json=payload)

    assert response.status_code == 200
    assert "anonymized_text" in response.json()
    mock_anonymize.assert_called_once_with(payload["text"])


@patch("app.anonymizer_service.anonymize")
def test_anonymize_failure(mock_anonymize):
    mock_anonymize.side_effect = Exception("Anonymizer failed")

    payload = {
        "text": "ذهبت بالأمس مع ركان إلى دكان السعداء"
    }

    response = client.post("/api/anonymize", json=payload)

    assert response.status_code == 500
