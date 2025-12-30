import pytest
import requests
from unittest.mock import patch, MagicMock
from src.orchestration_service import orchestration_service
from src.exceptions import ServiceException
from src.config import BACKEND_SERVICE_URL  

# Mock data
PHONE_NUMBER = "1234567890"
AUDIO_B64 = "ZmFrZS1hdWRpbw=="
TRANSCRIPTION = "Hello testing one two three."
ANONYMIZED = "Hello testing [REDACTED]."
TOKEN = "fake-jwt-token"

@pytest.fixture
def mock_requests_post():
    with patch("src.orchestration_service.requests.post") as mock:
        yield mock

@pytest.mark.unit
def test_login_success(mock_requests_post):
    mock_login = MagicMock()
    mock_login.status_code = 200
    mock_login.json.return_value = {"token": TOKEN}
    mock_requests_post.return_value = mock_login
    
    result = orchestration_service.login_by_phone(PHONE_NUMBER)
    assert result == TOKEN
    mock_requests_post.assert_called_once_with(
        f"{BACKEND_SERVICE_URL}/api/patient/login-by-phone-number",
        json={"phone_number": PHONE_NUMBER}
    )

@pytest.mark.unit
def test_login_failure(mock_requests_post):
    mock_response = mock_requests_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Login failed")
    with pytest.raises(ServiceException):
        orchestration_service.login_by_phone(PHONE_NUMBER)

@pytest.mark.unit
def test_process_voice_note_success(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.status_code = 200
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    
    mock_anon = MagicMock()
    mock_anon.status_code = 200
    mock_anon.json.return_value = {"anonymized_text": ANONYMIZED}
    
    mock_note = MagicMock()
    mock_note.status_code = 201
    mock_note.json.return_value = {"status": "Note added"}
    mock_requests_post.side_effect = [mock_stt, mock_anon, mock_note]

    result = orchestration_service.process_voice_note(TOKEN, AUDIO_B64)
    assert result == {"status": "success"}
    assert mock_requests_post.call_count == 3
    calls = mock_requests_post.call_args_list
    note_call_args = calls[2]
    assert note_call_args.kwargs['json'] == {"note": ANONYMIZED}
    assert note_call_args.kwargs['headers'] == {"Authorization": f"Bearer {TOKEN}"}

@pytest.mark.unit
def test_process_voice_note_stt_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.raise_for_status.side_effect = requests.exceptions.HTTPError("STT Failed")
    mock_requests_post.side_effect = [mock_stt]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(TOKEN, AUDIO_B64)
    assert "STT Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 1

@pytest.mark.unit
def test_process_voice_note_anonymization_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    
    mock_anon = MagicMock()
    mock_anon.raise_for_status.side_effect = requests.exceptions.HTTPError("Anon Failed")
    
    mock_requests_post.side_effect = [mock_stt, mock_anon]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(TOKEN, AUDIO_B64)
    assert "Anonymization Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 2

@pytest.mark.unit
def test_process_voice_note_create_note_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    mock_anon = MagicMock()
    mock_anon.json.return_value = {"anonymized_text": ANONYMIZED}
    mock_note = MagicMock()
    mock_note.raise_for_status.side_effect = requests.exceptions.HTTPError("Create Note Failed")
    
    mock_requests_post.side_effect = [mock_stt, mock_anon, mock_note]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(TOKEN, AUDIO_B64)
    assert "Create Note Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 3