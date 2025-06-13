import re

from rest_framework import serializers
from .models import CV


class CVSerializer(serializers.ModelSerializer):
    """
    Serializer for the CV model, including all fields and custom contacts validation.
    """
    class Meta:
        model = CV
        fields = "__all__"

    def validate_contacts(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Contacts must be a JSON object (dict).")

        required = ["email", "phone"]
        for field in required:
            if field not in value:
                raise serializers.ValidationError(f"Contacts must include '{field}'.")
            if not isinstance(value[field], str):
                raise serializers.ValidationError(f"'{field}' must be a string.")

        email = value["email"]
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.fullmatch(email_pattern, email):
            raise serializers.ValidationError("Invalid email address format.")

        phone = value["phone"]
        phone_pattern = r"^\+\d[\d\s\-\(\)]{3,}$"
        if not re.fullmatch(phone_pattern, phone):
            raise serializers.ValidationError(
                "Phone number must start with '+' "
                "and contain at least one digit after '+'. "
            )

        return value
