from rest_framework import serializers

from .models import Feedback


class CreateFeedbackSerializer(serializers.ModelSerializer):
    # this captures the current authenticated user, preventing
    # user instance interferance
    class Meta:
        model = Feedback
        fields = ['user_from', 'title', 'message']
        read_only_fields = ('user_from',)

    def create(self, validated_data):
        feedback = Feedback(
            user_from=self.context['request'].user,
            title=validated_data['title'],
            message=validated_data['message'])
        feedback.save()
        return feedback


class ListFeedbackSerializer(serializers.ModelSerializer):
    # this captures the current authenticated user, preventing
    # user instance interferance
    user_from = serializers.StringRelatedField(
        read_only=True,)
    user_to = serializers.StringRelatedField(
        read_only=True,)

    class Meta:
        model = Feedback
        fields = ['id', 'user_from', 'user_to', 'title',
                  'message', 'has_replied', 'reply', 'feedback_id', 'created_at']


class AdminReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user_to', 'reply', 'has_replied']
        read_only_fields = ('user_to', 'has_replied',)
        extra_kwargs = {
            'reply': {'required': True},
        }

    def create(self, validated_data):
        feedback = Feedback(
            user_to=self.context['request'].user,
            has_replied=True,
            reply=validated_data['has_replied'])
        feedback.save()
        return feedback
