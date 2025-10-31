"""
ASGI config for joby_api project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')

application = get_asgi_application()
