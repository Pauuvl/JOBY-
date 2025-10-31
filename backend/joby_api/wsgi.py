"""
WSGI config for joby_api project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')

application = get_wsgi_application()
