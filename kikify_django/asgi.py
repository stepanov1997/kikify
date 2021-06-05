"""
ASGI config for kikify_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kikify_django.settings')

if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

application = get_asgi_application()
