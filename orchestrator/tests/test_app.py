import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

@pytest.mark.unit
@patch("app.orchestration_service.process_voice_note")
@patch("app.orchestration_service.login_by_phone")
def test_process_note_success(mock_login_by_phone, mock_process_voice_note):
    mock_login_by_phone.return_value = "jwt-token"
    mock_process_voice_note.return_value = {"status": "success"}
    payload = {
        "phone_number": "1234567890",
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }
    response = client.post("/process_patient_note", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_login_by_phone.assert_called_once_with(payload["phone_number"])
    mock_process_voice_note.assert_called_once_with("jwt-token", payload["base64_audio"])

@pytest.mark.unit
@patch("app.orchestration_service.login_by_phone")
def test_process_note_login_failure(mock_login_by_phone):
    mock_login_by_phone.side_effect = Exception("Login failed")
    payload = {
        "phone_number": "1234567890",
        "base64_audio": "ZmFrZS1hdWRpbw=="
    }
    response = client.post("/process_patient_note", json=payload)
    assert response.status_code == 401

@pytest.mark.unit
@patch("app.greeting_service.greeting_msg", "Hello")
@patch("app.meta_service.send_message")
def test_greet_patient_success(mock_send_message):
    mock_send_message.return_value = {"status": "success"}
    payload = {
        "phone_number": "1234567890"
    }
    response = client.post("/greet_patient", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(payload["phone_number"], "Hello")

@pytest.mark.unit
@patch("app.meta_service.send_message")
def test_greet_patient_failure(mock_send_message):
    mock_send_message.side_effect = Exception("Greet Patient failed")
    payload = {
        "phone_number": "1234567890"
    }
    response = client.post("/greet_patient", json=payload)
    assert response.status_code == 500
