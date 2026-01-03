import pytest
from unittest.mock import MagicMock, patch
from src.meta_service import meta_service
from src.exceptions import ServiceException
import base64

@patch("src.meta_service.requests.post")
def test_send_template_message_success(mock_post):    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"messaging_product": "whatsapp", "contacts": [{"input": "123456789", "wa_id": "123456789"}], "messages": [{"id": "msg_123"}]}
    mock_post.return_value = mock_response
    response = meta_service.send_template_message(
            phone_number="123456789",
            template_name="test_template",
            template_language="en",
            template_params={"name": "test"}
    )
    assert response["messages"][0]["id"] == "msg_123"
    mock_post.assert_called_once()

@patch("src.meta_service.requests.post")
def test_send_thumbs_up_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_post.return_value = mock_response
    response = meta_service.send_thumbs_up("123456789", "msg_123")
    assert response["success"] is True
    mock_post.assert_called_once()

@patch("src.meta_service.requests.get")
@patch("src.meta_service.meta_service.meta_api_key", "test_key")
def test_get_media_as_base64_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake_audio_content"
    mock_get.return_value = mock_response
    expected_base64 = base64.b64encode(b"fake_audio_content").decode('utf-8')
    result = meta_service.get_media_as_base64("http://media.url")
    assert result == expected_base64
    mock_get.assert_called_once_with("http://media.url", headers={
        "Authorization": "Bearer test_key",
        "Content-Type": "application/json"
    })

@patch("src.meta_service.requests.post")
def test_send_template_message_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = Exception("Service Down")
    with pytest.raises(ServiceException) as excinfo:
        meta_service.send_template_message("123456789", "test", "en", {})

@patch("src.meta_service.requests.post")
def test_send_thumbs_up_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = Exception("Service Down")
    with pytest.raises(ServiceException) as excinfo:
        meta_service.send_thumbs_up("123456789", "msg_123")

@patch("src.meta_service.requests.get")
def test_get_media_as_base64_failure(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = Exception("Service Down")
    with pytest.raises(ServiceException) as excinfo:
        meta_service.get_media_as_base64("http://media.url")
