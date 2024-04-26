from django.urls import path
from . import views

urlpatterns = [
    # Task-related URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),

    # Notification-related URLs
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),

    # Feedback-related URLs
    path('feedback/', views.FeedbackListView.as_view(), name='feedback_list'),

    # Community-related URLs
    path('community/', views.CommunityListView.as_view(), name='community_list'),
    path('community/<int:pk>/', views.CommunityDetailView.as_view(), name='community_detail'),

    # URL for creating tasks via API
    path('api/tasks/', views.TaskListView.as_view(), name='task_create_api'),
]