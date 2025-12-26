# test anonymizer
from src.anonymizer import anonymizer_service

def test_anonymize():
    text= "ذهبت بالأمس مع ركان إلى دكان السعداء"
    anonymized_text = anonymizer_service.anonymize(text)
    assert "ركان" not in anonymized_text
    assert "السعداء" not in anonymized_text