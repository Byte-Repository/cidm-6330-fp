"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.core.asgi import get_asgi_application
core_asgi_app = get_asgi_application()

from channels.routing import ChannelNameRouter, ProtocolTypeRouter

from app1 import consumers


# for channels support
application = ProtocolTypeRouter(
    {
        "http": core_asgi_app,
        "channel": ChannelNameRouter(
            {
                 "Notification": consumers.TaskNotificationConsumer.as_asgi()
            }
        ),
    }
)
