from src.meta_service import meta_service
import pytest

@pytest.mark.integration
def test_send_template_message():
    response = meta_service.send_template_message("96171177395", "greet_patient", "ar", {"domain": "http://example.com", "code": "8Jx320E22"})
    assert type(response) == dict