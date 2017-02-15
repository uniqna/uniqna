from rest_framework import serializers
from threads.models import answer
from ask.models import tag, question


class AnswerSerializer(serializers.ModelSerializer):
	ups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	downs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = answer
		fields = ("id", "ups", "downs", "points")


class QuestionSerializer(serializers.ModelSerializer):
	ups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	downs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = question
		fields = ("id", "ups", "downs", "points")


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = tag
		fields = '__all__'
