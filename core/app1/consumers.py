import json
import asyncio
import datetime

from channels.consumer import AsyncConsumer
from channels.generic.http import AsyncHttpConsumer

from app1.models import Notification, Feedback, Community # Import necessary models

class TaskSucceededConsumer(AsyncConsumer):
    async def task_succeeded(self, event):
        print("Task succeeded")

class TaskNotificationConsumer(AsyncHttpConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}_notifications",
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}_notifications",
            self.channel_name
        )

    async def send_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

    async def receive(self, event):
        # Not handling incoming messages for notifications, 
        # as they will be pushed from the server side

        # Fetch notifications from models and send them
        notifications = Notification.objects.filter(user=self.user)
        for notification in notifications:
            await asyncio.sleep(0)  # Simulate async operation
            await self.send_notification({'notification': notification.message})
class TaskFeedbackConsumer(AsyncConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_feedback(self, event):
        feedback = event['feedback']
        await self.send(text_data=json.dumps({
            'type': 'feedback',
            'feedback': feedback
        }))

    async def receive(self, event):
        # Not handling incoming messages for feedback, 
        # as they will be pushed from the server side

        # Fetch feedback from models and send them
        feedbacks = Feedback.objects.filter(user=self.user)
        for feedback in feedbacks:
            await asyncio.sleep(0)  # Simulate async operation
            await self.send_feedback({'feedback': feedback.comment})

class CommunityChatConsumer(AsyncConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    async def receive(self, event):
        # Not handling incoming messages for chat, 
        # as they will be pushed from the server side

        # Fetch community messages from models and send them
        # You need to define the logic to fetch community messages
        # You might need to define a separate model for community messages

        # Placeholder for future implementation
        pass
