"""
WSGI config for diversion_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diversion_system.settings')

application = get_wsgi_application() 