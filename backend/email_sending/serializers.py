from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """
    Serializer for email sending request data.
    """

    email = serializers.EmailField(required=True)
