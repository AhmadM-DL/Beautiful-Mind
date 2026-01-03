import pytest
from unittest.mock import MagicMock, patch
from src.orchestrator_service import orchestrator_service
from src.exceptions import ServiceException

@patch("src.orchestrator_service.requests.post")
def test_process_voice_note_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response
    response = orchestrator_service.process_voice_note(
        phone_number="123456789",
        base64_audio="abc123base64"
    )
    assert response["status"] == "success"
    mock_post.assert_called_once()

@patch("src.orchestrator_service.requests.post")
def test_process_voice_note_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = Exception("Service Down")
    with pytest.raises(ServiceException):
        orchestrator_service.process_voice_note("123456789", "base64")
