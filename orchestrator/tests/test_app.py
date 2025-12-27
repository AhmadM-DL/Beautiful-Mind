import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

@patch("app.orchestration_service.process_voice_note")
def test_process_note_success(mock_process_note):
    mock_process_note.return_value = {"status": "success"}
    payload = {
        "phone_number": "1234567890",
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }
    response = client.post("/process_patient_note", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_process_note.assert_called_once_with(payload["phone_number"], payload["base64_audio"])

@patch("app.orchestration_service.process_voice_note")
def test_process_note_failure(mock_process_note):
    mock_process_note.side_effect = Exception("Process Note failed")
    payload = {
        "phone_number": "1234567890",
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }
    response = client.post("/process_patient_note", json=payload)
    assert response.status_code == 500