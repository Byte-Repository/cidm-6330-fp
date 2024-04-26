from rest_framework import serializers
from .models import Task, Notification, Feedback, Community, Priority
from .permissions import IsTaskOwner
from django.contrib.auth.models import User

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer()
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = ['id', 'description', 'assigned_user', 'deadline', 'priority']
        read_only_fields = ['assigned_user']  # Make assigned_user read-only

    def validate(self, data):
        # Example of simple permission logic
        user = self.context['request'].user
        assigned_user = data.get('assigned_user')

        # Check if the current user is the owner of the task
        if user != assigned_user:
            raise serializers.ValidationError("You are not authorized to assign tasks to other users.")

        return data

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    task = TaskSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'task', 'comment']

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description']
