import pytest
from unittest.mock import MagicMock, patch
from src.messages_service import response_messages_service

@pytest.mark.unit
def test_get_message_success():
    message = response_messages_service.get_message()
    assert message in response_messages_service.messages