from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task, Notification, Feedback, Community
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .permissions import IsTaskOwner

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwner]  # Apply custom permission

def home(request):
    tasks = Task.objects.all()
    notifications = Notification.objects.filter(user=request.user)
    feedback = Feedback.objects.filter(user=request.user)
    return render(request, 'home.html', {'tasks': tasks, 'notifications': notifications, 'feedback': feedback})

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

class NotificationListView(ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback_list.html'
    context_object_name = 'feedback'

class CommunityListView(ListView):
    model = Community
    template_name = 'community_list.html'
    context_object_name = 'communities'

class CommunityDetailView(DetailView):
    model = Community
    template_name = 'community_detail.html'
    context_object_name = 'community'
