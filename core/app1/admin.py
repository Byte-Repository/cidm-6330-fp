from django.contrib import admin
from .models import Task, Notification, Feedback, Community, Priority

admin.site.register(Task)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Community)
admin.site.register(Priority)
