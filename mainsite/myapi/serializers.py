from rest_framework import serializers
from .models import Observation, Target


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = "__all__"
