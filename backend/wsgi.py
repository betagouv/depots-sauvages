from os import environ
from pathlib import Path
from sys import path as sys_path

from django.core.wsgi import get_wsgi_application

# Django apps live in a subfolder that needs to be added to sys path
sys_path.append(str(Path(__file__).parent.parent / "backend"))

# This will set production as default, but we must still define it
# in env to ensure that the migrate command runs agains the correct DB
environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")

application = get_wsgi_application()
