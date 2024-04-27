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
    assigned_user = IsTaskOwner()
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = ['id', 'description', 'assigned_user', 'deadline', 'priority']
        read_only_fields = ['assigned_user']

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
