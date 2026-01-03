import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app
from src.config import META_HANDSHAKE_SECRET

client = TestClient(app)

@patch("app.meta_service")
def test_greet_patient_success(mock_meta):
    headers = {"Authorization": f"Bearer {META_HANDSHAKE_SECRET}"}
    payload = {
            "phone_number": "123456789",
            "url": "http://example.com",
            "password": "secret_password"
        }
    response = client.post("/greet_patient", json=payload, headers=headers)
    assert response.status_code == 200
    assert mock_meta.send_template_message.call_count == 2

def test_greet_patient_unauthorized():
    payload = {
        "phone_number": "123456789",
        "url": "http://example.com",
        "password": "secret_password"
    }
    response = client.post("/greet_patient", json=payload, headers={"Authorization": "Bearer wrong_token"})
    assert response.status_code == 401

def test_webhook_handshake_success():
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": META_HANDSHAKE_SECRET,
        "hub.challenge": "12345"
    }
    response = client.get("/webhook", params=params)
    assert response.status_code == 200
    assert response.text == "12345"

# fix order
@patch("app.meta_service")
@patch("app.orchestrator_service")
def test_webhook_audio_message(mock_orch, mock_meta):
    mock_meta.get_media_as_base64.return_value = "base64audio"
    
    payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "entry_id",
                "changes": [{
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {"phone_number_id": "id", "display_phone_number": "num"},
                        "messages": [{
                            "from": "123456789",
                            "id": "msg_id",
                            "timestamp": "123456",
                            "type": "audio",
                            "audio": {
                                "id": "audio_id",
                                "url": "http://audio.url",
                                "voice": "true"
                            }
                        }]
                    }
                }]
            }]
    }
    
    response = client.post("/webhook", json=payload)
    
    assert response.status_code == 200
    mock_meta.get_media_as_base64.assert_called_with("http://audio.url")
    mock_orch.process_voice_note.assert_called_with("123456789", "base64audio")
    mock_meta.send_thumbs_up.assert_called_with("123456789", "msg_id")

def test_webhook_no_messages():
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "entry_id",
            "changes": [{
                "field": "messages",
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"phone_number_id": "id", "display_phone_number": "num"},
                    "messages": []
                }
            }]
        }]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
