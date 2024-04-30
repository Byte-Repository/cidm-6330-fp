"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from app1.views import TaskListView, TaskDetailView, NotificationListView, FeedbackListView, CommunityListView, CommunityDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('communities/', CommunityListView.as_view(), name='community_list'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community_detail'),

    # Include the URLs for the app1 app
    path('', include('app1.urls')),
]

