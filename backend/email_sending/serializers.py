from django.conf import settings
from rest_framework import serializers

from backend.antispam_timer.timer import FormTimer


class EmailSerializer(serializers.Serializer):
    """
    Serializer for email sending request data.
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if request:
            FormTimer.validate_timer(request, settings.TIMER_BASE_NAME)
        return attrs
