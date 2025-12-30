from src.meta_service import MetaService
import pytest
from unittest.mock import patch
from src.exceptions import ServiceException
import requests

@pytest.fixture
def service():
    return MetaService("jwt-token", "phone-number")

@pytest.mark.unit
@patch("src.meta_service.requests.post")
def test_meta_service_send_message_success(mock_post, service):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {}

    service.send_message("1234567890", "Hello")
    mock_post.assert_called_once_with(
        "https://graph.facebook.com/v24.0/phone-number/messages",
        headers={"Authorization": "Bearer jwt-token", "Content-Type": "application/json"},
        json={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "1234567890",
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hello"
            }
        }
    )

@pytest.mark.unit
@patch("src.meta_service.requests.post")
def test_meta_service_send_message_failure(mock_post, service):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Meta Service Error")
    with pytest.raises(ServiceException):
        service.send_message("1234567890", "Hello")

