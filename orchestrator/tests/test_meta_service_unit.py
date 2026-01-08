from src.meta_service import meta_service
import pytest
from unittest.mock import patch
from src.exceptions import ServiceException
import requests

@pytest.mark.unit
@patch("src.meta_service.requests.post")
@patch("src.meta_service.meta_service.whatsapp_service_url", "http://whatsapp:8000")
@patch("src.meta_service.meta_service.handshake_secret", "meta_handshake_secret")
@patch("src.meta_service.meta_service.app_domain", "http://domain.com")
def test_meta_service_greet_patient_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {}

    meta_service.greet_patient("1234567890", "Hello")
    mock_post.assert_called_once_with(
        "http://whatsapp:8000/greet_patient",
        headers={"Authorization": "Bearer meta_handshake_secret", "Content-Type": "application/json"},
        json={
            "phone_number": "1234567890",
            "password": "Hello",
            "url": "http://domain.com"
        }
    )

@pytest.mark.unit
@patch("src.meta_service.requests.post")
def test_meta_service_greet_patient_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Meta Service Error")
    with pytest.raises(ServiceException):
        meta_service.greet_patient("1234567890", "Hello")

