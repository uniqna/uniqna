from rest_framework import serializers
from .models import answer


class AnswerSerializer(serializers.ModelSerializer):
	ups = serializers.StringRelatedField(many=True)
	downs = serializers.StringRelatedField(many=True)

	class Meta:
		model = answer
		fields = ("id", "ups", "downs")
