import pytest
import requests
from unittest.mock import patch, MagicMock
from src.orchestration_service import orchestration_service
from src.exceptions import ServiceException

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

def test_process_voice_note_success(mock_requests_post):

    # Setup mock responses for the chain of events
    
    # 1. STT
    mock_stt = MagicMock()
    mock_stt.status_code = 200
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    
    # 2. Anonymize
    mock_anon = MagicMock()
    mock_anon.status_code = 200
    mock_anon.json.return_value = {"anonymized_text": ANONYMIZED}
    
    # 3. Login
    mock_login = MagicMock()
    mock_login.status_code = 200
    mock_login.json.return_value = {"token": TOKEN}
    
    # 4. Add Voice Note
    mock_note = MagicMock()
    mock_note.status_code = 201
    mock_note.json.return_value = {"status": "Voice note added"}

    # Register the side effects in order
    mock_requests_post.side_effect = [mock_stt, mock_anon, mock_login, mock_note]

    # Execute
    result = orchestration_service.process_voice_note(PHONE_NUMBER, AUDIO_B64)

    # Assertions
    assert result == {"status": "success"}
    assert mock_requests_post.call_count == 4
    
    # Verify calls are made with correct parameters
    calls = mock_requests_post.call_args_list
    
    # Verify Login call (3rd) uses phone number
    login_call_args = calls[2]
    assert login_call_args.kwargs['json'] == {"phone_number": PHONE_NUMBER}
    
    # Verify Add Voice Note call (4th) uses anonymized text and token
    note_call_args = calls[3]
    assert note_call_args.kwargs['json'] == {"voice_note": ANONYMIZED}
    assert note_call_args.kwargs['headers'] == {"Authorization": f"Bearer {TOKEN}"}

def test_process_voice_note_stt_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.raise_for_status.side_effect = requests.exceptions.HTTPError("STT Failed")
    mock_requests_post.side_effect = [mock_stt]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(PHONE_NUMBER, AUDIO_B64)
    
    assert "STT Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 1

def test_process_voice_note_anonymization_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    
    mock_anon = MagicMock()
    mock_anon.raise_for_status.side_effect = requests.exceptions.HTTPError("Anon Failed")
    
    mock_requests_post.side_effect = [mock_stt, mock_anon]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(PHONE_NUMBER, AUDIO_B64)
    
    assert "Anonymization Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 2

def test_process_voice_note_login_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    mock_anon = MagicMock()
    mock_anon.json.return_value = {"anonymized_text": ANONYMIZED}
    
    mock_login = MagicMock()
    mock_login.raise_for_status.side_effect = requests.exceptions.HTTPError("Login Failed")
    
    mock_requests_post.side_effect = [mock_stt, mock_anon, mock_login]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(PHONE_NUMBER, AUDIO_B64)
    
    assert "Backend Login Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 3

def test_process_voice_note_create_note_failure(mock_requests_post):
    mock_stt = MagicMock()
    mock_stt.json.return_value = {"transcription": TRANSCRIPTION}
    mock_anon = MagicMock()
    mock_anon.json.return_value = {"anonymized_text": ANONYMIZED}
    mock_login = MagicMock()
    mock_login.json.return_value = {"token": TOKEN}
    
    mock_note = MagicMock()
    mock_note.raise_for_status.side_effect = requests.exceptions.HTTPError("Create Note Failed")
    
    mock_requests_post.side_effect = [mock_stt, mock_anon, mock_login, mock_note]

    with pytest.raises(ServiceException) as excinfo:
        orchestration_service.process_voice_note(PHONE_NUMBER, AUDIO_B64)
    
    assert "Create Voice Note Error" in str(excinfo.value)
    assert mock_requests_post.call_count == 4