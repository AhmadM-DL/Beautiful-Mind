import re
from rest_framework import serializers

def validate_phone_number(value):
    if not re.match(r'^\+?[1-9]\d{7,14}$', value):
        raise serializers.ValidationError("Invalid phone number")