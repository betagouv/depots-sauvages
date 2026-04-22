from rest_framework import serializers
from backend.procedures.models import SuiviProcedure

class SuiviProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviProcedure
        fields = '__all__'
        read_only_fields = ("created", "modified")
