from src.meta_service import meta_service
from src.greeting_service import greeting_service
import pytest

from logging import getLogger
logger = getLogger(__name__)

@pytest.mark.integration
def test_meta_service_send_message_success():
    response = meta_service.send_message("96171177395", greeting_service.greeting_msg)
    logger.info(response)